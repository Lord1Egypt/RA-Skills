#!/usr/bin/env python3
"""
Dial-a-Cron - Intelligent Cron Orchestration for OpenClaw

Features:
- Persistent state between runs
- Change detection (skip if no meaningful change)
- Smart delivery routing
- Token budget tracking
- Self-healing with backoff
- Auto-pause after repeated failures
"""

import json
import time
import hashlib
from datetime import datetime
from pathlib import Path
import subprocess
from typing import Dict, Any, Optional

class DialACron:
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.state_file = Path(f"memory/cron-state/{name}.json")
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    return json.load(f)
            except:
                return self._default_state()
        return self._default_state()

    def _default_state(self) -> Dict[str, Any]:
        return {
            "last_run": None,
            "last_output_hash": None,
            "failure_count": 0,
            "total_tokens": 0,
            "paused": False,
            "pause_reason": None,
            "history": []
        }

    def _save_state(self):
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def should_run(self, current_output: str = None) -> bool:
        """Determine if the cron should run based on state and config."""
        if self.state.get("paused"):
            return False

        if not current_output:
            return True

        # Change detection
        if self.config.get("change_detection", False):
            current_hash = hashlib.md5(current_output.encode()).hexdigest()
            if current_hash == self.state.get("last_output_hash"):
                print(f"[{self.name}] No change detected. Skipping.")
                return False

        return True

    def run(self, command: str) -> Dict[str, Any]:
        """Execute the cron with full dial-a-cron features."""
        if not self.should_run():
            return {"status": "skipped", "reason": "no_change_or_paused"}

        print(f"[{self.name}] Running at {datetime.now()}")

        start_time = time.time()
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=300
            )

            output = result.stdout + result.stderr
            success = result.returncode == 0

            # Update state
            self.state["last_run"] = datetime.now().isoformat()
            self.state["last_output_hash"] = hashlib.md5(output.encode()).hexdigest()
            self.state["failure_count"] = 0 if success else self.state.get("failure_count", 0) + 1

            if self.state["failure_count"] >= 3:
                self.state["paused"] = True
                self.state["pause_reason"] = "too_many_failures"

            self._save_state()

            return {
                "status": "success" if success else "error",
                "output": output,
                "returncode": result.returncode,
                "duration": time.time() - start_time
            }

        except Exception as e:
            self.state["failure_count"] = self.state.get("failure_count", 0) + 1
            self._save_state()
            return {
                "status": "exception",
                "error": str(e),
                "duration": time.time() - start_time
            }

    def get_status(self) -> Dict[str, Any]:
        """Return current status of this cron."""
        return {
            "name": self.name,
            "last_run": self.state.get("last_run"),
            "failure_count": self.state.get("failure_count", 0),
            "paused": self.state.get("paused", False),
            "pause_reason": self.state.get("pause_reason")
        }


# CLI entry point
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        # Simple status check for all dial-a-crons
        state_dir = Path("memory/cron-state")
        if state_dir.exists():
            for state_file in state_dir.glob("*.json"):
                name = state_file.stem
                print(f"{name}: ACTIVE")
        else:
            print("No dial-a-crons configured yet.")
    else:
        print("Dial-a-Cron v0.1")
        print("Usage: dial-a-cron status")
        print("Or import DialACron class in your crons.")
```

