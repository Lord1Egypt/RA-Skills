"""AgentPathfinder v2 — Task decomposition and state management (Phases 1-5)."""
import json
import os
import tempfile
import uuid
import time
import secrets
import logging
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Any, Optional
from enum import Enum

try:
    import fcntl
    _HAS_FCNTL = True
except ImportError:
    _HAS_FCNTL = False  # Windows — advisory locking disabled

from .pathfinder_core import (
    generate_master_key, split_key, hash_key,
    shard_to_hex, shard_from_hex, reconstruct_key,
    hmac_sign, derive_key
)
from .audit_trail import AuditTrail
from .tool_audit import ToolAuditChain

logger = logging.getLogger(__name__)


class TaskState(Enum):
    REGISTERED = "registered"
    DISPATCHED = "dispatched"
    IN_PROGRESS = "in_progress"
    STEP_COMPLETE = "step_complete"
    STEP_FAILED = "step_failed"
    STEP_RUNNING = "step_running"       # Phase 2: a step is actively executing
    PAUSED = "paused"
    RECONSTRUCTING = "reconstructing"
    TASK_COMPLETE = "task_complete"
    RECONSTRUCTION_FAILED = "reconstruction_failed"
    ABORTED = "aborted"


class TaskEngine:
    """Manages task lifecycle: creation, execution, state transitions."""

    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path.home() / ".agentpathfinder" / "pathfinder_data"
        self.data_dir = Path(data_dir)
        self.tasks_dir = self.data_dir / "tasks"
        self.vault_dir = self.data_dir / "vault"
        self.agents_dir = self.data_dir / "agents"
        self.tasks_dir.mkdir(parents=True, exist_ok=True)
        self.vault_dir.mkdir(parents=True, exist_ok=True)
        self.agents_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Atomic writes (Phase 2)
    # ------------------------------------------------------------------
    def _atomic_write(self, path, data):
        """Atomic file write: write to temp + os.rename (same filesystem)."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp_path = tempfile.mkstemp(dir=str(path.parent), suffix=".tmp")
        try:
            if isinstance(data, str):
                os.write(fd, data.encode())
            else:
                os.write(fd, data)
            os.fsync(fd)
            os.close(fd)
            os.rename(tmp_path, str(path))
        except BaseException:
            try:
                os.close(fd)
            except OSError:
                pass
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
            raise

    # ------------------------------------------------------------------
    # File locking (Phase 3)
    # ------------------------------------------------------------------
    @contextmanager
    def _lock_task(self, task_id: str):
        """Exclusive advisory lock on a task's lock file (no-op on Windows)."""
        if not _HAS_FCNTL:
            yield  # Windows — no advisory locking
            return
        lock_path = self.tasks_dir / f"{task_id}.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_fd = open(lock_path, "w")
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()

    @contextmanager
    def _lock_vault_shard(self, task_id: str, step_number: int):
        """Exclusive advisory lock on a vault shard file (no-op on Windows)."""
        if not _HAS_FCNTL:
            yield  # Windows — no advisory locking
            return
        lock_dir = self.vault_dir / task_id
        lock_dir.mkdir(parents=True, exist_ok=True)
        lock_path = lock_dir / f"{step_number}.shard.lock"
        lock_fd = open(lock_path, "w")
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            lock_fd.close()

    # ------------------------------------------------------------------
    # Vault helpers
    # ------------------------------------------------------------------
    def _get_vault_path(self, task_id: str, step_number: int) -> Path:
        """Get the filesystem path for a step's shard vault."""
        task_vault = self.vault_dir / task_id
        task_vault.mkdir(parents=True, exist_ok=True)
        return task_vault / f"{step_number}.shard"

    def _write_shard_to_vault(self, task_id: str, step_number: int, shard: bytes):
        """Write a step shard to the vault filesystem (atomic + locked)."""
        with self._lock_vault_shard(task_id, step_number):
            vault_path = self._get_vault_path(task_id, step_number)
            self._atomic_write(vault_path, shard)

    def _read_shard_from_vault(self, task_id: str, step_number: int) -> bytes:
        """Read a step shard from the vault filesystem (locked)."""
        with self._lock_vault_shard(task_id, step_number):
            vault_path = self._get_vault_path(task_id, step_number)
            if not vault_path.exists():
                raise FileNotFoundError(
                    f"Shard not found in vault for task {task_id} step {step_number}"
                )
            return vault_path.read_bytes()

    # ------------------------------------------------------------------
    # Audit key derivation (Phase 4)
    # ------------------------------------------------------------------
    def _derive_audit_key(self, master_key: bytes) -> bytes:
        """Derive a separate audit signing key from the master key.

        Phase 4: The audit trail must never have access to the master key.
        We use derive_key(master_key, b'audit_signing_key').
        """
        return derive_key(master_key, b"audit_signing_key")

    def _reconstruct_master_key(self, task: Dict[str, Any]) -> bytes:
        """Reconstruct master key from vault shards + issuer shard."""
        shards = [
            self._read_shard_from_vault(task["task_id"], step["step_number"])
            for step in task["steps"]
        ]
        shards.append(shard_from_hex(task["issuer_shard"]))
        return reconstruct_key(shards)

    def get_tool_audit(self, task_id: str, step_number: int) -> "ToolAuditChain":
        """Get a ToolAuditChain for tracking tool calls in a step.

        Example:
            audit = engine.get_tool_audit("tsk_abc", 1)
            tool_id = audit.log_tool_call("exec", {"command": "ls -la"})
            result = subprocess.run(...)
            audit.log_tool_result(tool_id, result.stdout)
        """
        task = self.get_task(task_id)
        master_key = self._reconstruct_master_key(task)
        audit_key = self._derive_audit_key(master_key)
        audit_trail = AuditTrail(
            self.data_dir / "audit" / f"{task_id}.jsonl", audit_key
        )
        return ToolAuditChain(task_id, step_number, audit_trail)

    # ------------------------------------------------------------------
    # Core CRUD
    # ------------------------------------------------------------------
    def create_task(self, name: str, steps: List[Dict[str, Any]]) -> str:
        """Create a new task. Step shards written to vault, NOT in task JSON."""
        task_id = str(uuid.uuid4())
        num_steps = len(steps)

        # Generate master key and shards
        master_key = generate_master_key()
        step_shards, issuer_shard = split_key(master_key, num_steps)

        # Phase 1: Write step shards to vault (atomic, Phase 2)
        for i, shard in enumerate(step_shards, start=1):
            self._write_shard_to_vault(task_id, i, shard)

        # Build task metadata (NO step shards in task JSON)
        task = {
            "task_id": task_id,
            "name": name,
            "state": TaskState.REGISTERED.value,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "num_steps": num_steps,
            "key_hash": hash_key(master_key),
            "issuer_shard": shard_to_hex(issuer_shard),
            "completed_steps": 0,
            "failed_steps": 0,
            "steps": [
                {
                    "step_number": i + 1,
                    "name": step["name"],
                    "state": "pending",
                    "token_id": None,
                    "result_hash": None,
                    "error": None,
                    "retry_count": 0,
                    "idempotency_key": None,    # Phase 2
                }
                for i, step in enumerate(steps)
            ],
        }

        # Save task metadata (atomic, Phase 2)
        task_path = self.tasks_dir / f"{task_id}.json"
        self._atomic_write(task_path, json.dumps(task, indent=2, default=str))

        # Phase 4: Derive audit key from master key
        audit_key = self._derive_audit_key(master_key)

        # Initialize audit trail
        audit = AuditTrail(
            self.data_dir / "audit" / f"{task_id}.jsonl", audit_key
        )
        audit.log(
            "TASK_REGISTERED",
            task_id,
            name=name,
            steps=num_steps,
            key_hash=task["key_hash"],
        )

        return task_id

    def get_task(self, task_id: str) -> Dict[str, Any]:
        """Load task metadata by ID."""
        task_path = self.tasks_dir / f"{task_id}.json"
        if not task_path.exists():
            raise ValueError(f"Task {task_id} not found")
        with open(task_path) as f:
            return json.load(f)

    def _save_task_unlocked(self, task: Dict[str, Any]):
        """Save task state atomically (no lock — caller must hold lock)."""
        task_path = self.tasks_dir / f"{task['task_id']}.json"
        self._atomic_write(task_path, json.dumps(task, indent=2, default=str))

    def save_task(self, task: Dict[str, Any]):
        """Save task state (atomic + locked, Phases 2-3)."""
        with self._lock_task(task["task_id"]):
            self._save_task_unlocked(task)

    def get_step_shard(self, task_id: str, step_number: int) -> bytes:
        """Retrieve a step shard from the vault."""
        return self._read_shard_from_vault(task_id, step_number)

    # ------------------------------------------------------------------
    # Step state transitions (Phase 2)
    # ------------------------------------------------------------------
    def set_step_running(self, task_id: str, step_number: int,
                         idempotency_key: str) -> str:
        """Mark step as 'running' with an idempotency key.

        Returns the idempotency_key on success.
        Raises ValueError if the step is already running with a *different* key
        (concurrent duplicate) or if the step is not in a launchable state.
        """
        with self._lock_task(task_id):
            task = self.get_task(task_id)
            step = task["steps"][step_number - 1]

            if step["state"] == "running":
                if step.get("idempotency_key") == idempotency_key:
                    # Same execution — idempotent, skip
                    return idempotency_key
                raise ValueError(
                    f"Step {step_number} already running with different "
                    f"idempotency key (conflict)"
                )

            if step["state"] not in ("pending",):
                raise ValueError(
                    f"Step {step_number} cannot transition to running "
                    f"(current: {step['state']})"
                )

            step["state"] = "running"
            step["idempotency_key"] = idempotency_key
            task["state"] = TaskState.IN_PROGRESS.value

            self._save_task_unlocked(task)

        return idempotency_key

    def detect_crashed_steps(self, task_id: str) -> List[Dict[str, Any]]:
        """Find steps stuck in 'running' state (crash recovery).

        Returns a list of step dicts that are still in 'running' state.
        The caller should decide whether to reset them to 'pending' or
        mark them as 'failed'.
        """
        task = self.get_task(task_id)
        return [
            step for step in task["steps"]
            if step["state"] == "running"
        ]

    def reset_running_step(self, task_id: str, step_number: int):
        """Reset a stuck 'running' step back to 'pending' (crash recovery)."""
        with self._lock_task(task_id):
            task = self.get_task(task_id)
            step = task["steps"][step_number - 1]
            if step["state"] != "running":
                raise ValueError(
                    f"Step {step_number} is not running (current: {step['state']})"
                )
            step["state"] = "pending"
            step["idempotency_key"] = None
            self._save_task_unlocked(task)

    # ------------------------------------------------------------------
    # Status & recovery
    # ------------------------------------------------------------------
    def get_status(self, task_id: str) -> Dict[str, Any]:
        """Get human-readable task status."""
        task = self.get_task(task_id)

        step_statuses = []
        for step in task["steps"]:
            step_statuses.append(
                {
                    "step_number": step["step_number"],
                    "name": step["name"],
                    "state": step["state"],
                    "token_id": step.get("token_id"),
                    "error": step.get("error"),
                }
            )

        return {
            "task_id": task_id,
            "name": task["name"],
            "overall_state": task["state"],
            "progress": f"{task['completed_steps']}/{task['num_steps']}",
            "steps": step_statuses,
            "all_complete": task["completed_steps"] == task["num_steps"],
        }

    def reset_step(self, task_id: str, step_number: int) -> Dict[str, Any]:
        """Reset a failed step to pending so it can be retried."""
        task = self.get_task(task_id)
        step = task["steps"][step_number - 1]

        if step["state"] != "failed":
            raise ValueError(
                f"Step {step_number} is not failed (current: {step['state']})"
            )

        step["state"] = "pending"
        step["error"] = None
        step["retry_count"] = 0
        step["idempotency_key"] = None

        task["failed_steps"] = max(0, task["failed_steps"] - 1)
        task["state"] = "in_progress"

        self.save_task(task)

        # Log retry attempt with audit key
        master_key = self._reconstruct_master_key(task)
        audit_key = self._derive_audit_key(master_key)
        audit = AuditTrail(
            self.data_dir / "audit" / f"{task_id}.jsonl", audit_key
        )
        audit.log("STEP_RETRY_INITIATED", task_id, step_number=step_number)

        return step

    def resume_from_failure(self, task_id: str) -> Optional[int]:
        """Find the first failed step and return its number for retry."""
        task = self.get_task(task_id)

        for step in task["steps"]:
            if step["state"] == "failed":
                self.reset_step(task_id, step["step_number"])
                return step["step_number"]

        return None

    # ------------------------------------------------------------------
    # Agent registry (Phase 5)
    # ------------------------------------------------------------------
    def _agents_file(self) -> Path:
        return self.agents_dir / "registry.json"

    def _load_agents(self) -> Dict[str, str]:
        """Load agent registry {agent_id: api_key_hex}."""
        path = self._agents_file()
        if not path.exists():
            return {}
        with open(path) as f:
            return json.load(f)

    def _save_agents(self, agents: Dict[str, str]):
        self._atomic_write(self._agents_file(), json.dumps(agents, indent=2))

    def register_agent(self, agent_id: str) -> str:
        """Register an agent and return its API key (hex-encoded shared secret).

        If the agent already exists, the existing key is returned.
        """
        agents = self._load_agents()
        if agent_id in agents:
            return agents[agent_id]

        api_key = secrets.token_hex(32)  # 256-bit shared secret
        agents[agent_id] = api_key
        self._save_agents(agents)
        logger.info("Registered agent %s", agent_id)
        return api_key

    def verify_agent(self, agent_id: str, api_key: str) -> bool:
        """Verify agent credentials (constant-time comparison)."""
        agents = self._load_agents()
        expected = agents.get(agent_id)
        if expected is None:
            return False
        import hmac as _hmac
        return _hmac.compare_digest(expected, api_key)

    def authenticate_agent_request(self, agent_id: str, payload: str,
                                   signature: str) -> bool:
        """Verify an HMAC-signed request from an agent.

        The agent signs the payload with its API key (as raw bytes).
        """
        agents = self._load_agents()
        api_key_hex = agents.get(agent_id)
        if api_key_hex is None:
            return False
        api_key_bytes = bytes.fromhex(api_key_hex)
        return hmac_sign(api_key_bytes, payload) == signature  # constant-time inside hmac_sign/verify
