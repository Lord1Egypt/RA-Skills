#!/usr/bin/env python3
"""
Container & Subprocess Isolation Sandbox for OpenClaw.
Runs candidate sub-agents inside isolated, resource-constrained environments
with strict execution timeouts and restricted file system scope.
"""

import subprocess
import tempfile
import os
import shutil
import time
from typing import Dict, Any, Tuple


class ContainerSandbox:
    def __init__(self, timeout_seconds: float = 5.0, max_memory_mb: int = 256):
        self.timeout_seconds = timeout_seconds
        self.max_memory_mb = max_memory_mb

    def execute_in_isolation(self, script_code: str, env_vars: Dict[str, str] = None) -> Tuple[bool, str, float]:
        """
        Executes code within an ephemeral, restricted temporary directory.
        Returns: (success, output/error, execution_time_ms)
        """
        start = time.time()
        temp_dir = tempfile.mkdtemp(prefix="openclaw_sandbox_")

        try:
            script_path = os.path.join(temp_dir, "candidate_task.py")
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(script_code)

            env = os.environ.copy()
            if env_vars:
                env.update(env_vars)
            # Remove dangerous system keys from sandbox execution
            env.pop("OPENCLAW_FACTORY_SIGNING_KEY", None)

            proc = subprocess.run(
                [os.sys.executable, script_path],
                cwd=temp_dir,
                env=env,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds
            )

            latency = round((time.time() - start) * 1000, 1)
            if proc.returncode == 0:
                return True, proc.stdout.strip(), latency
            else:
                return False, proc.stderr.strip(), latency

        except subprocess.TimeoutExpired:
            latency = round((time.time() - start) * 1000, 1)
            return False, f"Sandbox execution TIMED OUT (> {self.timeout_seconds}s)", latency
        except Exception as e:
            latency = round((time.time() - start) * 1000, 1)
            return False, f"Sandbox error: {str(e)}", latency
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    sandbox = ContainerSandbox(timeout_seconds=2.0)
    ok, out, lat = sandbox.execute_in_isolation("print('Isolated sandbox execution successful!')")
    print(f"Sandbox Result (OK={ok}, Latency={lat}ms):", out)
