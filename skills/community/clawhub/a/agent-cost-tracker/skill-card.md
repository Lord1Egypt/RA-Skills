## Description:

Estimates LLM token costs and tallies spend from local agent run logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itspremkumar](https://clawhub.ai/user/itspremkumar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, FinOps teams, and agent operators use this skill to estimate token costs before a run and tally local agent log spending afterward. It is best treated as a basic local estimator rather than a complete budget-alerting or finance export system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation includes a curl command for downloading and running unpinned remote Python code.

Mitigation: Prefer the packaged agent_cost_tracker.py file, or require a pinned commit and checksum before executing a downloaded copy.

Risk: The packaged CI verification script can execute local Python files in folders it checks.

Mitigation: Run ci/verify_product.py only in a sandboxed environment with no secrets or network access when checking untrusted folders.

Risk: Advertised budget alerts and CSV export are not fully supported by the packaged tracker behavior.

Mitigation: Rely on the skill for local estimation and tallying only unless budget-alert and export behavior has been separately verified.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/itspremkumar/skills/agent-cost-tracker)
- [Packaged README](artifact/README.md)
- [Packaged Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands; CLI output as plain text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python 3.8+ and does not call model provider APIs.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter is 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
