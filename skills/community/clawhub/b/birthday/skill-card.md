## Description:

Helps agents manage Chinese lunar and solar birthday reminders, extract birthdays from Chinese ID numbers, set per-record advance reminder windows, and generate due or upcoming reminder results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[web3aivc](https://clawhub.ai/user/web3aivc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain structured birthday records, convert between lunar and solar birthday dates, import birthday data from Chinese ID numbers, and run reminder checks locally or through an explicitly configured notification channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store names, birthdays, and masked ID-derived data in a local JSON file.

Mitigation: Use the local record and check features only when storing this personal data locally is acceptable.

Risk: The skill can suggest creation of a recurring OpenClaw automation for daily reminder checks.

Mitigation: Allow the agent to create the recurring automation only when daily background checks are explicitly wanted.

Risk: Configured email or webhook channels can transmit personal reminder data outside the local environment.

Mitigation: Enable outbound notification channels only after verifying destinations, limiting message contents, and handling SMTP credentials through a secure environment or secret manager.

## Reference(s):

- [Data format reference](references/data-format.md)
- [ClawHub skill page](https://clawhub.ai/web3aivc/skills/birthday)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose a daily OpenClaw automation when the local data file first receives a record; email and webhook notification channels require explicit user configuration.]

## Skill Version(s):

1.0.1 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
