"""AgentPathfinder v2 — Issuing layer: shard vault, token issuance, validation (Phases 1-5)."""
import json
import time
import uuid
import logging
from pathlib import Path
from typing import Dict, Any, Optional

from .pathfinder_core import (
    hmac_sign, verify_hmac, shard_from_hex, shard_to_hex,
    reconstruct_key, hash_key
)
from .audit_trail import AuditTrail
from .task_engine import TaskEngine

logger = logging.getLogger(__name__)


class IssuingLayer:
    """
    Trusted component that:
    - Holds issuer_shard (in task JSON, never distributed to agents)
    - Manages step shards in vault filesystem (Phase 1)
    - Validates step results
    - Issues signed step tokens upon successful completion
    - Logs all events to audit trail
    - Optionally authenticates agents (Phase 5)
    """

    def __init__(self, task_engine: TaskEngine):
        self.task_engine = task_engine

    # ------------------------------------------------------------------
    # Phase 5: Agent authentication helper
    # ------------------------------------------------------------------
    def verify_agent_auth(self, agent_id: str, payload: str,
                          signature: str) -> bool:
        """Verify an agent's HMAC-signed request before token issuance.

        Returns True if the agent is registered and the signature is valid.
        """
        return self.task_engine.authenticate_agent_request(
            agent_id, payload, signature
        )

    # ------------------------------------------------------------------
    # Token issuance
    # ------------------------------------------------------------------
    def issue_step_token(self, task_id: str, step_number: int,
                         result: Any, result_hash: str,
                         agent_id: str = None,
                         agent_signature: str = None) -> Optional[Dict[str, Any]]:
        """
        Validate step result and issue signed token.

        Phase 1: Step shard read from vault, NOT from task JSON.
        Phase 2: Accepts steps in 'pending' or 'running' state.
        Phase 5: If agent_id is provided, verifies auth before issuance.
        """
        # Phase 5: optional agent authentication
        if agent_id is not None:
            payload = f"{task_id}:{step_number}:{result_hash}"
            if agent_signature is None:
                raise ValueError("agent_signature required when agent_id is provided")
            if not self.verify_agent_auth(agent_id, payload, agent_signature):
                raise PermissionError(
                    f"Agent '{agent_id}' authentication failed for step {step_number}"
                )
        else:
            logger.debug(
                "issue_step_token called without agent_id for task %s step %d "
                "(auth not enforced)", task_id, step_number
            )

        task = self.task_engine.get_task(task_id)
        step = task["steps"][step_number - 1]

        # Phase 2: allow both 'pending' and 'running' states
        if step["state"] not in ("pending", "running"):
            raise ValueError(
                f"Step {step_number} is not pending/running (current: {step['state']})"
            )

        # Generate token ID
        token_id = f"tok_{uuid.uuid4().hex[:12]}"

        # Phase 1: Load shards from vault for signing
        issuer_shard = shard_from_hex(task["issuer_shard"])
        step_shard = self.task_engine.get_step_shard(task_id, step_number)

        # Create token payload
        token = {
            "task_id": task_id,
            "step_number": step_number,
            "step_name": step["name"],
            "shard_hash": hash_key(step_shard),  # Phase 1: only expose hash
            "result_hash": result_hash,
            "token_id": token_id,
            "issued_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

        # Sign token with combined key material
        signing_key = issuer_shard + step_shard
        token["issuer_signature"] = hmac_sign(
            signing_key,
            f"{task_id}:{step_number}:{step['name']}:{result_hash}",
        )

        # Update task state
        step["state"] = "complete"
        step["token_id"] = token_id
        step["result_hash"] = result_hash
        step["idempotency_key"] = None  # clear running key
        task["completed_steps"] += 1

        # Check if all steps complete
        if task["completed_steps"] == task["num_steps"]:
            task["state"] = "reconstructing"
        else:
            task["state"] = "in_progress"

        self.task_engine.save_task(task)

        # Log to audit (Phase 4: use audit key, not master key)
        master_key = self._reconstruct_master_key(task)
        audit_key = self.task_engine._derive_audit_key(master_key)
        audit = AuditTrail(
            self.task_engine.data_dir / "audit" / f"{task_id}.jsonl", audit_key
        )
        audit.log(
            "STEP_COMPLETE",
            task_id,
            step_number=step_number,
            result_hash=result_hash,
            token_id=token_id,
        )

        return token

    def reconstruct_master_key(self, task_id: str) -> Optional[bytes]:
        """
        Reconstruct master key from all step tokens + issuer shard.
        Phase 1: Reads step shards from vault.
        Returns key bytes or None if incomplete.
        """
        task = self.task_engine.get_task(task_id)

        if task["completed_steps"] != task["num_steps"]:
            return None

        # Phase 1: Collect all shards from vault
        shards = [
            self.task_engine.get_step_shard(task_id, step["step_number"])
            for step in task["steps"]
        ]
        shards.append(shard_from_hex(task["issuer_shard"]))

        reconstructed = reconstruct_key(shards)

        # Verify hash
        expected_hash = hash_key(reconstructed)

        if expected_hash != task["key_hash"]:
            # Tamper detected!
            master_key = self._reconstruct_master_key(task)
            audit_key = self.task_engine._derive_audit_key(master_key)
            audit = AuditTrail(
                self.task_engine.data_dir / "audit" / f"{task_id}.jsonl",
                audit_key,
            )
            audit.log(
                "RECONSTRUCTION_FAILED",
                task_id,
                reason="hash_mismatch",
                expected=task["key_hash"],
                got=expected_hash,
            )
            task["state"] = "reconstruction_failed"
            self.task_engine.save_task(task)
            return None

        # Success
        task["state"] = "task_complete"
        self.task_engine.save_task(task)

        master_key = self._reconstruct_master_key(task)
        audit_key = self.task_engine._derive_audit_key(master_key)
        audit = AuditTrail(
            self.task_engine.data_dir / "audit" / f"{task_id}.jsonl", audit_key
        )
        audit.log("TASK_COMPLETE", task_id, key_hash=task["key_hash"])

        return reconstructed

    def _reconstruct_master_key(self, task) -> bytes:
        """Internal: reconstruct key from task data for audit signing.
        Phase 1: Reads step shards from vault."""
        shards = [
            self.task_engine.get_step_shard(task["task_id"], step["step_number"])
            for step in task["steps"]
        ]
        shards.append(shard_from_hex(task["issuer_shard"]))
        return reconstruct_key(shards)

    def fail_step(self, task_id: str, step_number: int, error: str):
        """Mark step as failed."""
        task = self.task_engine.get_task(task_id)
        step = task["steps"][step_number - 1]

        step["state"] = "failed"
        step["error"] = error
        step["retry_count"] += 1
        step["idempotency_key"] = None  # clear running key
        task["failed_steps"] += 1
        task["state"] = "paused"

        self.task_engine.save_task(task)

        # Log with audit key
        master_key = self._reconstruct_master_key(task)
        audit_key = self.task_engine._derive_audit_key(master_key)
        audit = AuditTrail(
            self.task_engine.data_dir / "audit" / f"{task_id}.jsonl", audit_key
        )
        audit.log("STEP_FAILED", task_id, step_number=step_number, error=error)
