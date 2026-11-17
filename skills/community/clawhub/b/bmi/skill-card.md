## Description:

Logs and exports local BMI and fitness tracking notes, with commands for goals, trends, summaries, search, and recent activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to record, search, summarize, and export local weight or fitness tracking notes. Review before relying on it for actual BMI calculations or charts, because the security evidence says it mainly saves free-form notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is advertised as BMI calculation and charting, but security evidence says it mainly stores free-form health log notes.

Mitigation: Review outputs before relying on them for BMI calculations or charts; use a validated calculator for health decisions.

Risk: Health-adjacent notes are stored persistently as plaintext under ~/.local/share/bmi.

Mitigation: Avoid entering sensitive health details on shared systems; restrict permissions, back up deliberately, or delete the local data directory when no longer needed.

## Reference(s):

- [Bmi ClawHub Skill Page](https://clawhub.ai/bytesagain-lab/skills/bmi)
- [BytesAgain Homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Plain text CLI output with optional JSON, CSV, or TXT export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores persistent local logs under ~/.local/share/bmi]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
