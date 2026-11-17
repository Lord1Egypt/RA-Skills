## Description:

Scans GitHub for zero-comment open issues, filters candidates by repository signals, stores them in a local queue, and provides a tracker for PR status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to find open GitHub issues, triage candidate repositories, and maintain a local queue or PR-status tracker before deciding whether to engage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is advertised as full issue-claiming and PR-submission automation, while the shipped scripts primarily scan, filter, queue issues, and track PR status.

Mitigation: Treat the skill as a scanner and local tracker until the documentation and scripts are corrected and any claiming or PR submission steps are verified manually.

Risk: The documentation encourages unattended cron execution and the configuration defaults imply automatic claiming and submitting.

Mitigation: Run with manual review first, avoid cron-based unattended execution, and do not grant broad GitHub permissions unless the workflow has been reviewed and constrained.

Risk: The authoritative security guidance identifies a queue-file update race or symlink issue.

Mitigation: Keep data files in a trusted, access-controlled directory and avoid concurrent runs until queue-file handling is fixed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/auto-bounty-hunter)
- [Publisher profile](https://clawhub.ai/user/dagangtj)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON queue files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses GitHub CLI and jq; writes queue, history, and log files under a local data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
