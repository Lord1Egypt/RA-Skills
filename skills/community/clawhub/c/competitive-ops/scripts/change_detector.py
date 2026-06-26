#!/usr/bin/env python3
"""Change detector for monitoring competitor changes."""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ChangeResult:
    changed: bool
    change_type: str  # "added", "removed", "modified", "unchanged"
    old_value: Any
    new_value: Any
    change_percent: float


class ChangeDetector:
    """Detect changes between snapshots."""

    def __init__(self, threshold: float = 0.05):
        self.threshold = threshold  # 5% change threshold

    def detect_change(self, old: Any, new: Any) -> ChangeResult:
        """Detect if old and new values have significant difference.

        Args:
            old: Previous value (dict, list, str, or number)
            new: New value

        Returns:
            ChangeResult with change details
        """
        if type(old) != type(new):
            return ChangeResult(
                changed=True,
                change_type="modified",
                old_value=old,
                new_value=new,
                change_percent=100.0
            )

        if isinstance(old, dict):
            return self._detect_dict_change(old, new)
        elif isinstance(old, list):
            return self._detect_list_change(old, new)
        else:
            return self._detect_scalar_change(old, new)

    def _detect_dict_change(self, old: dict, new: dict) -> ChangeResult:
        all_keys = set(old.keys()) | set(new.keys())
        changes = 0

        for key in all_keys:
            if key not in old:
                changes += 1
            elif key not in new:
                changes += 1
            elif old[key] != new[key]:
                changes += 1

        change_percent = changes / len(all_keys) if all_keys else 0

        return ChangeResult(
            changed=change_percent >= self.threshold,
            change_type="modified",
            old_value=old,
            new_value=new,
            change_percent=change_percent * 100
        )

    def _detect_list_change(self, old: list, new: list) -> ChangeResult:
        added = len(set(new) - set(old))
        removed = len(set(old) - set(new))
        change_percent = (added + removed) / max(len(old), len(new), 1)

        return ChangeResult(
            changed=change_percent >= self.threshold,
            change_type="modified",
            old_value=old,
            new_value=new,
            change_percent=change_percent * 100
        )

    def _detect_scalar_change(self, old: Any, new: Any) -> ChangeResult:
        if isinstance(old, (int, float)) and isinstance(new, (int, float)):
            if old == 0:
                change_percent = abs(new) * 100 if new != 0 else 0
            else:
                change_percent = abs((new - old) / old) * 100
        else:
            change_percent = 0 if old == new else 100

        return ChangeResult(
            changed=change_percent >= (self.threshold * 100),
            change_type="modified" if old != new else "unchanged",
            old_value=old,
            new_value=new,
            change_percent=change_percent
        )
