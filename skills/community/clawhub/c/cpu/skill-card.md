## Description:

Cpu provides shell commands for recording, searching, exporting, and reviewing timestamped local operations journal entries for CPU and system operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain3](https://clawhub.ai/user/bytesagain3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators can use this skill to log, search, export, and review local notes about system scans, alerts, fixes, backups, benchmarks, and related operations. It should be used as a local journal rather than as an actual CPU monitor.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CPU-monitoring branding may lead users to expect live telemetry or resource analysis.

Mitigation: Treat the skill as a local operations journal and verify CPU, load, temperature, and process data with trusted system monitoring tools.

Risk: Local logs and exported files may retain sensitive operational notes.

Mitigation: Avoid recording secrets, tokens, customer data, private incident details, or sensitive infrastructure notes, and review ~/.local/share/cpu plus exported files before sharing or backing them up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bytesagain3/skills/cpu)
- [Publisher profile](https://clawhub.ai/user/bytesagain3)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and a shell script artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes local plain-text logs and optional JSON, CSV, or TXT exports under ~/.local/share/cpu.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and script report 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
