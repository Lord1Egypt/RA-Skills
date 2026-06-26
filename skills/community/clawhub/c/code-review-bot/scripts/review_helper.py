import argparse
import json
from pathlib import Path


def load_json(path_value):
    path = Path(path_value)
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def summarize_risk(pr_data, checks):
    risk_signals = []
    if pr_data.get("changedFiles", 0) >= 20:
        risk_signals.append("large file surface")
    if pr_data.get("additions", 0) >= 500:
        risk_signals.append("high addition count")
    if pr_data.get("deletions", 0) >= 250:
        risk_signals.append("high deletion count")
    if pr_data.get("isDraft"):
        risk_signals.append("draft pull request")
    if pr_data.get("mergeable") not in {"MERGEABLE", "MERGE_QUEUEABLE"}:
        risk_signals.append(f'mergeable={pr_data.get("mergeable", "UNKNOWN")}')

    failing = [check for check in checks if check.get("bucket") == "fail" or check.get("state") == "FAILURE"]
    pending = [check for check in checks if check.get("bucket") == "pending" or check.get("state") == "PENDING"]
    if failing:
        risk_signals.append("failing checks present")
    if pending:
        risk_signals.append("pending checks remain")
    return risk_signals, failing, pending


def render_markdown(pr_data, checks):
    risk_signals, failing, pending = summarize_risk(pr_data, checks)
    author = pr_data.get("author", {}).get("login", "unknown")
    labels = ", ".join(label.get("name", "") for label in pr_data.get("labels", [])) or "none"
    lines = [
        f"# PR Review Pack: #{pr_data.get('number', '?')} {pr_data.get('title', 'Untitled PR')}",
        "",
        "## Overview",
        f"- Author: @{author}",
        f"- Branches: {pr_data.get('headRefName', '?')} -> {pr_data.get('baseRefName', '?')}",
        f"- Scope: {pr_data.get('changedFiles', 0)} files, +{pr_data.get('additions', 0)} / -{pr_data.get('deletions', 0)}",
        f"- Labels: {labels}",
        "",
        "## Risk Signals",
    ]
    if risk_signals:
        lines.extend(f"- {signal}" for signal in risk_signals)
    else:
        lines.append("- no automatic high-risk signals detected")

    lines.extend(["", "## Failing Checks"])
    if failing:
        lines.extend(
            f"- {check.get('name', 'unknown')} ({check.get('workflow', 'workflow')})"
            for check in failing
        )
    else:
        lines.append("- none")

    lines.extend(["", "## Pending Checks"])
    if pending:
        lines.extend(
            f"- {check.get('name', 'unknown')} ({check.get('workflow', 'workflow')})"
            for check in pending
        )
    else:
        lines.append("- none")

    lines.extend(
        [
            "",
            "## Suggested Review Plan",
            "- Verify the user-facing intent against the PR description.",
            "- Inspect the riskiest changed areas first.",
            "- Confirm failing checks are understood before recommending merge.",
            "- Call out missing tests, rollout risks, and open questions separately from hard blockers."
        ]
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Render a deterministic review summary from gh JSON output.")
    parser.add_argument("--pr-json", required=True, help="Path to gh pr view JSON output")
    parser.add_argument("--checks-json", required=True, help="Path to gh pr checks JSON output")
    args = parser.parse_args()

    pr_data = load_json(args.pr_json)
    checks = load_json(args.checks_json)
    print(render_markdown(pr_data, checks))


if __name__ == "__main__":
    main()
