#!/usr/bin/env python3
"""
Dial-a-Cron — State Manager (Phase 1)
Wraps OpenClaw cron jobs with persistent state, error tracking, and self-heal.

Usage (from a cron's pre-flight):
    from state import CronState
    s = CronState("helga-sync-rook")
    if s.should_skip():
        sys.exit(0)
    # ... do work ...
    s.finish(status="ok", output="3 docs synced", carry={"lastDocCount": 21264})

Usage (self-contained):
    python state.py <job-id> --status ok --output "3 docs synced"
    python state.py <job-id> --status error --output "connection refused"
    python state.py <job-id> --show
"""

import json
import os
import sys
import argparse
import hashlib
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = os.environ.get(
    "DAC_STATE_DIR",
    str(Path(__file__).parent.parent / "state")
)

SELF_HEAL_RULES = {
    1: "warn",     # Log warning, continue normally
    2: "minimal",  # Strip optional steps
    3: "pause",    # Pause job, alert owner
}

MAX_DELIVERY_HISTORY = 20


class CronState:
    def __init__(self, job_id: str):
        self.job_id = job_id
        self.path = Path(STATE_DIR) / f"{job_id}.json"
        self.data = self._load()

    def _load(self) -> dict:
        if self.path.exists():
            try:
                with open(self.path) as f:
                    return json.load(f)
            except Exception:
                pass
        return self._default()

    def _default(self) -> dict:
        return {
            "jobId": self.job_id,
            "lastRunAt": None,
            "lastStatus": None,
            "lastOutput": None,
            "lastHash": None,
            "consecutiveErrors": 0,
            "consecutiveNoOps": 0,
            "runCount": 0,
            "totalTokens": 0,
            "monthlyTokens": 0,
            "monthlyTokensMonth": datetime.now(timezone.utc).strftime("%Y-%m"),
            "carry": {},
            "paused": False,
            "pausedReason": None,
            "deliveryHistory": [],
        }

    def _save(self):
        Path(STATE_DIR).mkdir(parents=True, exist_ok=True)
        with open(self.path, "w") as f:
            json.dump(self.data, f, indent=2, default=str)

    def should_skip(self) -> bool:
        """Returns True if this job should be skipped (paused by self-heal)."""
        if self.data.get("paused"):
            print(f"[dial-a-cron] Job '{self.job_id}' is paused: {self.data.get('pausedReason')}", file=sys.stderr)
            return True
        return False

    def get_heal_level(self) -> str:
        """Return current self-heal level based on consecutive errors."""
        errors = self.data.get("consecutiveErrors", 0)
        if errors == 0:
            return "normal"
        return SELF_HEAL_RULES.get(errors, "pause")

    def get_carry(self) -> dict:
        """Return carry data from previous run."""
        return self.data.get("carry", {})

    def get_consecutive_errors(self) -> int:
        return self.data.get("consecutiveErrors", 0)

    def start(self):
        """Call at the beginning of a run. Increments run count."""
        self.data["runCount"] = self.data.get("runCount", 0) + 1
        # Reset monthly token counter if month changed
        current_month = datetime.now(timezone.utc).strftime("%Y-%m")
        if self.data.get("monthlyTokensMonth") != current_month:
            self.data["monthlyTokens"] = 0
            self.data["monthlyTokensMonth"] = current_month
        self._save()

    def finish(
        self,
        status: str,           # "ok" | "error" | "noop"
        output: str = "",
        carry: dict = None,
        tokens: int = 0,
        delivery_level: str = "silent",
        delivery_target: str = "log",
    ):
        """Call at the end of a run with results."""
        now = datetime.now(timezone.utc).isoformat()
        self.data["lastRunAt"] = now
        self.data["lastStatus"] = status
        self.data["lastOutput"] = output[:500] if output else ""
        self.data["totalTokens"] = self.data.get("totalTokens", 0) + tokens
        self.data["monthlyTokens"] = self.data.get("monthlyTokens", 0) + tokens

        if carry is not None:
            self.data["carry"] = carry

        if status == "ok":
            self.data["consecutiveErrors"] = 0
            self.data["consecutiveNoOps"] = 0
        elif status == "noop":
            self.data["consecutiveNoOps"] = self.data.get("consecutiveNoOps", 0) + 1
            self.data["consecutiveErrors"] = 0
        elif status == "error":
            errors = self.data.get("consecutiveErrors", 0) + 1
            self.data["consecutiveErrors"] = errors
            heal = SELF_HEAL_RULES.get(errors)
            if heal == "pause":
                self.data["paused"] = True
                self.data["pausedReason"] = f"Auto-paused after {errors} consecutive errors. Last: {output[:200]}"
                print(f"[dial-a-cron] ⚠️  Job '{self.job_id}' AUTO-PAUSED: {self.data['pausedReason']}", file=sys.stderr)

        # Track delivery history
        history = self.data.get("deliveryHistory", [])
        history.insert(0, {
            "at": now,
            "status": status,
            "to": delivery_target,
            "level": delivery_level,
        })
        self.data["deliveryHistory"] = history[:MAX_DELIVERY_HISTORY]
        self._save()

    def resume(self):
        """Manually resume a paused job."""
        self.data["paused"] = False
        self.data["pausedReason"] = None
        self.data["consecutiveErrors"] = 0
        self._save()
        print(f"[dial-a-cron] Job '{self.job_id}' resumed.")

    def show(self):
        """Print current state."""
        print(json.dumps(self.data, indent=2, default=str))

    def summary(self) -> str:
        """One-line status summary."""
        errors = self.data.get("consecutiveErrors", 0)
        paused = self.data.get("paused", False)
        last_run = self.data.get("lastRunAt", "never")
        last_status = self.data.get("lastStatus", "unknown")
        heal = self.get_heal_level()
        tokens_mo = self.data.get("monthlyTokens", 0)
        status_icon = "[OK]" if last_status == "ok" else "[ERR]" if last_status == "error" else "[--]"
        paused_str = " [PAUSED]" if paused else ""
        return (
            f"{status_icon} {self.job_id}{paused_str}: "
            f"last={last_status} errors={errors} heal={heal} "
            f"tokens/mo={tokens_mo:,} last_run={last_run[:19] if last_run else 'never'}"
        )


def list_all_jobs() -> list[CronState]:
    """Return CronState for all known jobs."""
    state_path = Path(STATE_DIR)
    if not state_path.exists():
        return []
    return [CronState(p.stem) for p in state_path.glob("*.json")]


def main():
    parser = argparse.ArgumentParser(description="Dial-a-Cron State Manager")
    parser.add_argument("job_id", nargs="?", help="Job ID")
    parser.add_argument("--status", choices=["ok", "error", "noop"], help="Set job status")
    parser.add_argument("--output", default="", help="Output message")
    parser.add_argument("--tokens", type=int, default=0, help="Tokens used this run")
    parser.add_argument("--carry", help="JSON carry data")
    parser.add_argument("--show", action="store_true", help="Show current state")
    parser.add_argument("--resume", action="store_true", help="Resume paused job")
    parser.add_argument("--list", action="store_true", help="List all job states")
    parser.add_argument("--heal-level", action="store_true", help="Print heal level and exit")
    args = parser.parse_args()

    if args.list:
        jobs = list_all_jobs()
        if not jobs:
            print("No jobs tracked yet.")
        for j in jobs:
            print(j.summary())
        return

    if not args.job_id:
        parser.print_help()
        return

    s = CronState(args.job_id)

    if args.show:
        s.show()
        return

    if args.resume:
        s.resume()
        return

    if args.heal_level:
        print(s.get_heal_level())
        return

    if args.status:
        carry = json.loads(args.carry) if args.carry else None
        s.start()
        s.finish(
            status=args.status,
            output=args.output,
            tokens=args.tokens,
            carry=carry,
        )
        print(s.summary())
        # Exit non-zero if paused (caller can check)
        if s.data.get("paused"):
            sys.exit(2)
    else:
        # Just show summary
        print(s.summary())


if __name__ == "__main__":
    main()
