#!/usr/bin/env python3
"""Render a markdown report from a browser evidence session manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def format_artifacts(artifacts: dict[str, str]) -> list[str]:
    parts: list[str] = []
    labels = {
        "screenshot": "screenshot",
        "dom_dump": "dom",
        "console_log": "console",
        "network_log": "network",
        "video": "video",
    }
    for key, label in labels.items():
        value = artifacts.get(key, "").strip()
        if value:
            parts.append(f"{label}: `{value}`")
    return parts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Session manifest JSON.")
    parser.add_argument("--out", required=True, help="Output markdown file.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = load_manifest(manifest_path)
    session = payload.get("session", {})
    summary = payload.get("summary", {})
    steps = payload.get("steps", [])

    lines = [
        "# Browser Proof Report",
        "",
        f"- Session: `{session.get('session_id', '')}`",
        f"- App: {session.get('app', '')}",
        f"- Goal: {session.get('goal', '')}",
        f"- Base URL: {session.get('base_url', '') or 'n/a'}",
        f"- Run context: {session.get('run_context', '') or 'n/a'}",
        f"- Environment: {session.get('environment', '') or 'n/a'}",
        f"- Surfaces: {', '.join(session.get('surfaces', [])) or 'n/a'}",
        f"- Overall status: **{summary.get('status', 'unknown')}**",
        f"- Passed / Failed / Blocked: {summary.get('passed_steps', 0)} / {summary.get('failed_steps', 0)} / {summary.get('blocked_steps', 0)}",
        "",
        "## Steps",
        "",
    ]

    for index, step in enumerate(steps, start=1):
        lines.append(f"### {index}. {step.get('step_id', f'step-{index}')}")
        lines.append(f"- Surface: {step.get('surface', '') or 'n/a'}")
        lines.append(f"- Status: **{step.get('status', 'unknown')}**")
        lines.append(f"- Action: {step.get('action', '')}")
        lines.append(f"- Expected: {step.get('expected', '')}")
        lines.append(f"- Actual: {step.get('actual', '')}")
        if step.get("note"):
            lines.append(f"- Note: {step['note']}")
        issue_keys = step.get("issue_keys", [])
        if issue_keys:
            lines.append(f"- Issue keys: {', '.join(issue_keys)}")
        artifact_parts = format_artifacts(step.get("artifacts", {}))
        if artifact_parts:
            lines.append(f"- Artifacts: {'; '.join(artifact_parts)}")
        lines.append("")

    if summary.get("issue_keys"):
        lines.extend(
            [
                "## Issue Keys",
                "",
                f"- {', '.join(summary['issue_keys'])}",
                "",
            ]
        )

    out_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
