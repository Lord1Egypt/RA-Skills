"""
Driftwatch — Bootstrap File Truncation Analysis

Reads all bootstrap files from the workspace, calculates per-file and
aggregate char counts, identifies truncation risk, and calculates
the 70/20/10 split zones. Character counting only — no token estimation.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from references.constants import (
    BOOTSTRAP_MAX_CHARS_PER_FILE,
    BOOTSTRAP_TOTAL_MAX_CHARS,
    TRUNCATION_HEAD_RATIO,
    TRUNCATION_TAIL_RATIO,
    BOOTSTRAP_FILE_ORDER,
)


def _file_status(char_count: int, limit: int) -> str:
    if char_count > limit:
        return "critical"
    pct = char_count / limit
    if pct > 0.80:
        return "warning"
    if pct > 0.60:
        return "info"
    return "ok"


def _aggregate_status(total_chars: int, aggregate_limit: int) -> str:
    if total_chars > aggregate_limit:
        return "critical"
    if total_chars / aggregate_limit > 0.75:
        return "warning"
    return "ok"


def analyze_truncation(workspace_path: str) -> dict:
    limit = BOOTSTRAP_MAX_CHARS_PER_FILE
    aggregate_limit = BOOTSTRAP_TOTAL_MAX_CHARS
    head_zone = int(limit * TRUNCATION_HEAD_RATIO)   # 14000
    tail_zone = int(limit * TRUNCATION_TAIL_RATIO)   # 4000

    files = []
    running_total = 0

    for idx, filename in enumerate(BOOTSTRAP_FILE_ORDER):
        filepath = os.path.join(workspace_path, filename)
        injection_order = idx + 1

        if not os.path.exists(filepath):
            entry = {
                "file": filename,
                "exists": False,
                "char_count": 0,
                "limit": limit,
                "percent_of_limit": 0.0,
                "status": "info",
                "message": "File not found — not contributing to budget but also not providing instructions",
                "head_zone_chars": head_zone,
                "tail_zone_chars": tail_zone,
                "truncated_middle_chars": 0,
                "injection_order": injection_order,
                "remaining_aggregate_budget_after": aggregate_limit - running_total,
            }
        else:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            char_count = len(content)
            running_total += char_count

            percent_of_limit = round((char_count / limit) * 100, 1)
            status = _file_status(char_count, limit)
            truncated_middle = max(0, char_count - head_zone - tail_zone)

            entry = {
                "file": filename,
                "exists": True,
                "char_count": char_count,
                "limit": limit,
                "percent_of_limit": percent_of_limit,
                "status": status,
                "head_zone_chars": head_zone,
                "tail_zone_chars": tail_zone,
                "truncated_middle_chars": truncated_middle,
                "injection_order": injection_order,
                "remaining_aggregate_budget_after": aggregate_limit - running_total,
            }

            if char_count == 0:
                entry["status"] = "info"
                entry["message"] = "File is empty"

        files.append(entry)

    total_chars = running_total
    percent_of_aggregate = round((total_chars / aggregate_limit) * 100, 1)
    aggregate_status = _aggregate_status(total_chars, aggregate_limit)

    # Sequential starvation: how much budget remains after first 7 files
    chars_first_7 = sum(f["char_count"] for f in files if f["injection_order"] <= 7)
    remaining_after_7 = aggregate_limit - chars_first_7
    last_file = BOOTSTRAP_FILE_ORDER[-1]

    # Only flag starvation when remaining budget is below the per-file limit
    if remaining_after_7 < BOOTSTRAP_MAX_CHARS_PER_FILE:
        starvation_risk = (
            f"{last_file} may receive reduced budget — "
            f"only {remaining_after_7} chars remain after first 7 files"
        )
    else:
        starvation_risk = None

    aggregate = {
        "total_chars": total_chars,
        "aggregate_limit": aggregate_limit,
        "percent_of_aggregate": percent_of_aggregate,
        "aggregate_status": aggregate_status,
    }
    if starvation_risk:
        aggregate["budget_starvation_risk"] = starvation_risk

    return {
        "files": files,
        "aggregate": aggregate,
    }
