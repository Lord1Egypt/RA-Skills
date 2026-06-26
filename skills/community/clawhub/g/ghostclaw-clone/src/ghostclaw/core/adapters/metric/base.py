"""Base utilities for Metric Adapters."""

import asyncio
import json
from typing import Dict, List, Any, Optional
from ghostclaw.core.adapters.base import MetricAdapter, AdapterMetadata

class AsyncProcessMetricAdapter(MetricAdapter):
    """
    Base MetricAdapter that provides common utilities for running 
    external tools via async subprocesses.
    """

    async def run_tool(self, cmd: List[str], cwd: Optional[str] = None, timeout: Optional[int] = None) -> Dict[str, Any]:
        """
        Safely execute an external tool and capture its output.
        Uses process.communicate() to avoid pipe deadlocks.
        """
        try:
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=cwd
            )
            
            try:
                if timeout is not None:
                    stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
                else:
                    stdout, stderr = await process.communicate()
            except asyncio.TimeoutError:
                try:
                    process.terminate()
                    await asyncio.wait_for(process.wait(), timeout=5)
                except ProcessLookupError:
                    pass
                except asyncio.TimeoutError:
                    process.kill()
                    await process.wait()
                return {"error": f"Tool timed out after {timeout}s", "returncode": -1, "timeout": True}
            
            return {
                "returncode": process.returncode,
                "stdout": (stdout or b"").decode().strip(),
                "stderr": (stderr or b"").decode().strip()
            }
        except Exception as e:
            return {"error": str(e), "returncode": -1}

    def parse_json(self, text: str) -> Optional[Dict[str, Any]]:
        """Safely parse JSON output from a tool."""
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
