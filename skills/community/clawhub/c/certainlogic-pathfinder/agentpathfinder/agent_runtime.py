"""AgentPathfinder v2 — Agent runtime: step execution wrapper (Phases 1-5)."""
import hashlib
import traceback
import uuid
from typing import Dict, Any, Callable, Optional

from .pathfinder_core import hmac_sign
from .task_engine import TaskEngine, TaskState
from .issuing_layer import IssuingLayer


class AgentRuntime:
    """
    Wraps agent step execution:
    - Receives step spec + shard
    - Executes step function
    - Validates result
    - Requests token from issuing layer
    - Optionally authenticates with agent_id / api_key (Phase 5)
    - Optionally notifies via callbacks (chat, webhooks, logging)
    """

    def __init__(self, task_engine: TaskEngine, issuing_layer: IssuingLayer,
                 agent_id: str = None, api_key: str = None,
                 on_step_complete: Callable[[int, Any], None] = None,
                 on_step_fail: Callable[[int, str], None] = None,
                 on_task_complete: Callable[[str, Dict[str, Any]], None] = None):
        self.task_engine = task_engine
        self.issuing = issuing_layer
        # Phase 5: optional agent credentials
        self.agent_id = agent_id
        self.api_key = api_key  # hex-encoded shared secret
        # Chat notification callbacks
        self.on_step_complete = on_step_complete
        self.on_step_fail = on_step_fail
        self.on_task_complete = on_task_complete

    def _sign_payload(self, payload: str) -> Optional[str]:
        """Sign a payload with the agent's API key (Phase 5)."""
        if self.api_key is None:
            return None
        api_key_bytes = bytes.fromhex(self.api_key)
        return hmac_sign(api_key_bytes, payload)

    def execute_step(self, task_id: str, step_number: int,
                     step_func: Callable, step_args: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Execute a single step with error handling.

        Phase 2: Sets step to 'running' before execution with an idempotency key.
        Returns result dict with status.
        """
        task = self.task_engine.get_task(task_id)
        step = task["steps"][step_number - 1]

        # Phase 1 fix: get shard from task_engine, not issuing layer
        shard = self.task_engine.get_step_shard(task_id, step_number)

        # Phase 2: transition to 'running' with idempotency key
        idem_key = str(uuid.uuid4())
        try:
            self.task_engine.set_step_running(task_id, step_number, idem_key)
        except ValueError:
            # Step might not be in a state that allows running transition
            # (e.g. already complete). Continue; issue_step_token will
            # raise a clear error if the state is truly wrong.
            pass

        result = {
            "task_id": task_id,
            "step_number": step_number,
            "step_name": step["name"],
            "status": "pending",
            "result": None,
            "error": None,
            "token": None,
        }

        try:
            # Execute step function
            print(
                f"  [Agent] Executing step {step_number}/{task['num_steps']}: "
                f"{step['name']}"
            )
            step_result = step_func(**(step_args or {}))

            # Hash result for verification
            result_str = str(step_result)
            result_hash = hashlib.sha256(result_str.encode()).hexdigest()[:16]

            # Phase 5: prepare auth parameters
            agent_id_param = self.agent_id
            agent_sig_param = None
            if self.agent_id and self.api_key:
                payload = f"{task_id}:{step_number}:{result_hash}"
                agent_sig_param = self._sign_payload(payload)

            # Request token from issuing layer
            token = self.issuing.issue_step_token(
                task_id, step_number, step_result, result_hash,
                agent_id=agent_id_param,
                agent_signature=agent_sig_param,
            )

            result["status"] = "complete"
            result["result"] = step_result
            result["token"] = token

            # Notify callback
            if self.on_step_complete:
                self.on_step_complete(step_number, step_result)

        except Exception as e:
            error_msg = f"{type(e).__name__}: {str(e)}"
            print(f"  [Agent] Step {step_number} FAILED: {error_msg}")
            result["status"] = "failed"
            result["error"] = error_msg

            # Notify callback
            if self.on_step_fail:
                self.on_step_fail(step_number, error_msg)

        return result

    def execute_task(self, task_id: str, step_functions: Dict[str, Callable],
                     max_retries: int = 3) -> Dict[str, Any]:
        """
        Execute all steps of a task sequentially.

        step_functions: Dict mapping step_name -> callable

        Returns final task status.
        """
        task = self.task_engine.get_task(task_id)

        print(f"\n[AgentRuntime] Starting task: {task['name']} ({task['num_steps']} steps)")

        for step in task["steps"]:
            step_number = step["step_number"]
            step_name = step["name"]

            if step_name not in step_functions:
                print(f"  Warning: No function bound for step '{step_name}', skipping")
                continue

            # Execute with retry logic
            retries = 0
            last_error = None
            while retries <= max_retries:
                result = self.execute_step(task_id, step_number, step_functions[step_name])

                if result["status"] == "complete":
                    break

                last_error = result["error"]
                retries += 1
                if retries <= max_retries:
                    print(
                        f"  [AgentRuntime] Retrying step {step_number} "
                        f"(attempt {retries + 1}/{max_retries + 1})"
                    )

            if result["status"] != "complete":
                if last_error:
                    self.issuing.fail_step(task_id, step_number, last_error)
                print(
                    f"\n[AgentRuntime] Task PAUSED — step {step_number} "
                    f"failed after {max_retries + 1} attempts"
                )
                return self.task_engine.get_status(task_id)

        # All steps complete — attempt reconstruction
        print(f"\n[AgentRuntime] All steps complete. Reconstructing key...")
        master_key = self.issuing.reconstruct_master_key(task_id)

        if master_key:
            print(f"  Task COMPLETE — key reconstructed successfully")
        else:
            print(f"  Task RECONSTRUCTION FAILED — tamper detected")

        status = self.task_engine.get_status(task_id)

        # Notify callback
        if self.on_task_complete:
            self.on_task_complete(task_id, status)

        return status

    def retry_step(self, task_id: str, step_number: int,
                   step_func: Callable, step_args: Dict[str, Any] = None,
                   max_retries: int = 3) -> Dict[str, Any]:
        """
        Retry a single failed step after human intervention.
        Resets the step to pending, then executes with retry logic.
        """
        step = self.task_engine.reset_step(task_id, step_number)
        print(f"\n[AgentRuntime] Retrying step {step_number}: {step['name']}")

        retries = 0
        last_error = None
        while retries <= max_retries:
            result = self.execute_step(task_id, step_number, step_func, step_args)

            if result["status"] == "complete":
                print(f"  [AgentRuntime] Step {step_number} retry SUCCESS")
                break

            last_error = result["error"]
            retries += 1
            if retries <= max_retries:
                print(f"  [AgentRuntime] Retry attempt {retries + 1}/{max_retries + 1}")

        if result["status"] != "complete":
            if last_error:
                self.issuing.fail_step(task_id, step_number, last_error)
            print(
                f"  [AgentRuntime] Step {step_number} retry FAILED "
                f"after {max_retries + 1} attempts"
            )

        # If this was the last failed step, check if all steps now complete
        task = self.task_engine.get_task(task_id)
        if task["completed_steps"] == task["num_steps"]:
            print(f"\n[AgentRuntime] All steps complete. Reconstructing key...")
            master_key = self.issuing.reconstruct_master_key(task_id)
            if master_key:
                print(f"  Task COMPLETE — key reconstructed successfully")
            else:
                print(f"  Task RECONSTRUCTION FAILED — tamper detected")

        return self.task_engine.get_status(task_id)

    def resume_task(self, task_id: str, step_functions: Dict[str, Callable],
                    max_retries: int = 3) -> Dict[str, Any]:
        """
        Resume a PAUSED task from the first failed step.
        """
        failed_step = self.task_engine.resume_from_failure(task_id)

        if failed_step is None:
            task = self.task_engine.get_task(task_id)
            print(f"\n[AgentRuntime] No failed steps found in task '{task['name']}'")

            if task["completed_steps"] == task["num_steps"]:
                print(f"  Task already complete ({task['num_steps']}/{task['num_steps']} steps)")
                return self.task_engine.get_status(task_id)
            else:
                print(f"  All steps are pending — use 'run' instead of 'resume'")
                return self.task_engine.get_status(task_id)

        print(f"\n[AgentRuntime] Resuming task from step {failed_step}...")

        task = self.task_engine.get_task(task_id)

        for step in task["steps"]:
            step_number = step["step_number"]
            step_name = step["name"]

            if step["state"] == "complete":
                continue

            if step_name not in step_functions:
                print(f"  Warning: No function bound for step '{step_name}', skipping")
                continue

            retries = 0
            while retries <= max_retries:
                result = self.execute_step(task_id, step_number, step_functions[step_name])

                if result["status"] == "complete":
                    break

                retries += 1
                if retries <= max_retries:
                    print(
                        f"  [AgentRuntime] Retrying step {step_number} "
                        f"(attempt {retries + 1}/{max_retries + 1})"
                    )

            if result["status"] != "complete":
                print(
                    f"\n[AgentRuntime] Task PAUSED — step {step_number} "
                    f"failed after {max_retries + 1} attempts"
                )
                return self.task_engine.get_status(task_id)

        # All steps complete
        print(f"\n[AgentRuntime] All steps complete. Reconstructing key...")
        master_key = self.issuing.reconstruct_master_key(task_id)

        if master_key:
            print(f"  Task COMPLETE — key reconstructed successfully")
        else:
            print(f"  Task RECONSTRUCTION FAILED — tamper detected")

        return self.task_engine.get_status(task_id)
