"""Markdown report helpers + file-output trailer + plan-tier message."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


def write_report(title: str, content: str, to_file: Path | None = None) -> str:
    report = f"# {title}\nGenerated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}\n\n{content}"
    if to_file:
        to_file.parent.mkdir(parents=True, exist_ok=True)
        to_file.write_text(report)
    return report


def render_feature_unavailable(
    feature: str,
    plan_required: str = "Plus",
    what_this_does: str = "",
) -> str:
    """Friendly markdown block for plan-tier-gated features.

    Use when a script hits a 403 on a plan-gated AC endpoint. The user's
    account simply isn't on a tier that exposes the feature — that's not a
    bug, so the script should print this block and exit 0 (cleanly), not
    raise. Avoids the word "ERROR" deliberately.
    """
    detail = f"\n*{what_this_does}*\n" if what_this_does else ""
    return (
        f"# Not available on your ActiveCampaign plan\n"
        f"\n"
        f"**{feature}** requires the **{plan_required}** plan or higher on "
        f"ActiveCampaign. Your current plan doesn't expose this endpoint, so "
        f"this report can't be generated.\n"
        f"{detail}\n"
        f"This isn't a bug — your account just isn't on a tier that includes "
        f"the feature. If you upgrade your AC plan, re-run the script and "
        f"it will work without changes.\n"
        f"\n"
        f"Other scripts in this skill that don't depend on **{feature}** will "
        f"still work normally.\n"
    )


def emit_files(*paths) -> None:
    """Emit a structured trailer line for every file written.

    Format:
      __SKILL_FILES__:["/abs/path/1","/abs/path/2"]

    Always prints to stdout so the harness captures it. Call AFTER any
    human-readable `Wrote /path` lines so both formats are available.
    """
    abs_paths = [str(Path(p).expanduser().resolve()) for p in paths]
    print(f"__SKILL_FILES__:{json.dumps(abs_paths)}")
