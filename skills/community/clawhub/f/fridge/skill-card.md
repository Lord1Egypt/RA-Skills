## Description:

Track fridge and pantry inventory with expiry reminders and grocery lists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and household maintainers use this skill to log fridge and pantry items, review recent activity, search entries, and export local inventory notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores fridge and household notes persistently in local logs.

Mitigation: Avoid storing sensitive personal data unless local persistent logs are acceptable, and manage access to ~/.local/share/fridge.

Risk: The skill description overstates expiry reminder and grocery-list automation.

Mitigation: Use it as a local logging and export aid, not as the source of truth for actual expiry-date reminders or grocery automation.

Risk: Exported JSON, CSV, or text files may contain untrusted or pasted entry content.

Mitigation: Review and sanitize exports before sharing them or importing them into spreadsheets and other tools.

## Reference(s):

- [Fridge on ClawHub](https://clawhub.ai/bytesagain-lab/skills/fridge)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text CLI output with optional JSON, CSV, or text export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local logs under ~/.local/share/fridge.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
