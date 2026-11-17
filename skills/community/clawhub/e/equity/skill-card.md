## Description:

Model cap tables, dilution scenarios, and vesting schedules for startups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and operators can use this skill for startup equity planning tasks such as cap table modeling, dilution scenarios, vesting schedules, option pricing, and local record export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive cap-table, fundraising, compensation, or ownership data may be stored in plaintext local log files.

Mitigation: Do not enter real sensitive equity data unless plaintext local storage is acceptable; use non-sensitive test data or a controlled data directory.

Risk: The available security assessment says the skill presents as an equity calculator but mainly stores and searches arbitrary local input.

Mitigation: Review behavior before relying on outputs for equity decisions, and confirm calculation, export, retention, and deletion behavior in a safe environment.

## Reference(s):

- [Equity Skill on ClawHub](https://clawhub.ai/bytesagain1/skills/equity)
- [BytesAgain](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local plaintext log and export files under ~/.local/share/equity unless EQUITY_DIR changes the data directory.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
