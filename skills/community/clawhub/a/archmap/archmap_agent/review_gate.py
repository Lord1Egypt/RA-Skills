from pathlib import Path
from typing import Callable


class ReviewGate:
    def __init__(self, on_approve: Callable | None = None, on_reject: Callable | None = None):
        self.on_approve = on_approve
        self.on_reject = on_reject

    def review(self, decision: str, context: dict | None = None) -> dict:
        decision = decision.lower()
        if decision == "approve":
            if self.on_approve:
                self.on_approve(context or {})
            return {"status": "approved", "action": "commit_baseline"}
        if decision == "reject":
            if self.on_reject:
                self.on_reject(context or {})
            return {"status": "rejected", "action": "discard_memory"}
        return {"status": "invalid", "action": "none"}
