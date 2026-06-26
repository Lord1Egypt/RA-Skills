#!/usr/bin/env python3
"""Validate a browser evidence bundle before sharing it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ARTIFACT_FIELDS = ("screenshot", "dom_dump", "console_log", "network_log", "video")


def add_finding(findings: list[dict], severity: str, code: str, message: str, step_id: str = "") -> None:
    findings.append(
        {
            "severity": severity,
            "code": code,
            "message": message,
            "step_id": step_id,
        }
    )


def load_manifest(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def is_absolute_or_private(path_text: str) -> bool:
    return path_text.startswith("/") or path_text.startswith("~") or ":\\" in path_text or path_text.startswith("file://")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Session manifest JSON.")
    parser.add_argument("--repo-root", default=".", help="Optional repo root for artifact existence checks.")
    parser.add_argument("--out", required=True, help="Output JSON report.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    repo_root = Path(args.repo_root).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    payload = load_manifest(manifest_path)
    findings: list[dict] = []

    session = payload.get("session", {})
    if not session.get("session_id"):
        add_finding(findings, "error", "missing-session-id", "Session ID is required.")
    if not session.get("app"):
        add_finding(findings, "error", "missing-app", "App name is required.")
    if not session.get("goal"):
        add_finding(findings, "error", "missing-goal", "Goal is required.")

    steps = payload.get("steps", [])
    if not steps:
        add_finding(findings, "error", "no-steps", "Bundle has no recorded steps.")

    for index, step in enumerate(steps, start=1):
        step_id = step.get("step_id", f"step-{index}")
        if not step.get("action"):
            add_finding(findings, "error", "missing-action", "Step is missing action text.", step_id)
        if not step.get("expected"):
            add_finding(findings, "error", "missing-expected", "Step is missing expected behavior.", step_id)
        if not step.get("actual"):
            add_finding(findings, "error", "missing-actual", "Step is missing actual behavior.", step_id)

        status = step.get("status")
        if status not in {"passed", "failed", "blocked"}:
            add_finding(findings, "error", "invalid-status", "Step status must be passed, failed, or blocked.", step_id)

        artifacts = step.get("artifacts", {})
        screenshot = artifacts.get("screenshot", "")
        if status in {"failed", "blocked"} and not screenshot:
            add_finding(findings, "warning", "missing-screenshot", "Failed or blocked step should include a screenshot.", step_id)

        if status == "failed" and not step.get("note") and not step.get("issue_keys"):
            add_finding(findings, "warning", "missing-failure-detail", "Failed step should include a note or issue key.", step_id)

        for field in ARTIFACT_FIELDS:
            artifact_path = artifacts.get(field, "").strip()
            if not artifact_path:
                continue
            if is_absolute_or_private(artifact_path):
                add_finding(findings, "error", "absolute-artifact-path", f"{field} uses an absolute or private path.", step_id)
                continue
            candidate = repo_root / artifact_path
            if not candidate.exists():
                add_finding(findings, "warning", "missing-artifact", f"{field} path does not exist under repo root: {artifact_path}", step_id)

    errors = sum(1 for finding in findings if finding["severity"] == "error")
    warnings = sum(1 for finding in findings if finding["severity"] == "warning")

    report = {
        "manifest": str(manifest_path),
        "repo_root": str(repo_root),
        "status": "ok" if errors == 0 else "fix_required",
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
    }
    out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
