## Description:

360Guard provides a checklist-driven security review workflow and local scan scripts for evaluating agent skills before installation or use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinc913](https://clawhub.ai/user/robinc913)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agent operators use this skill to review unknown or higher-risk skills before installation, combining manual checklist guidance with local quick, full, or Node.js scans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can report a clean result even when its simple scanners miss relevant executable files or patterns.

Mitigation: Treat scan output as heuristic triage only and require manual review or stronger security tooling before approving high-risk skills.

Risk: Example workflows for ClawHub and GitHub downloads can contact external services and clone or fetch untrusted code.

Mitigation: Run scans on local copies when possible, use network access deliberately, and inspect downloaded artifacts before execution.

Risk: The scanner writes full-scan reports into the scanned skill directory.

Mitigation: Scan disposable copies or review generated report files before keeping or publishing the scanned directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robinc913/skills/360guard-skillvetter-upgrade-version)
- [Publisher profile](https://clawhub.ai/user/robinc913)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown reports and terminal scan output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports classify findings by risk level and may include file paths, line numbers, snippets, and scan exit codes.]

## Skill Version(s):

1.0.0 (source: server release metadata and CHANGELOG, released 2026-03-13)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
