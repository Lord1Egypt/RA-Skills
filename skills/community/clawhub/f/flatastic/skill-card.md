## Description:

Manage shared household chores, shopping lists, and expenses via Flatastic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[david-schopf](https://clawhub.ai/user/david-schopf)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a Flatastic household use this skill to ask an agent for Flatastic CLI guidance that reads or updates chores, shopping items, expenses, balances, and bulletin-board messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external flatastic CLI that was not reviewed as part of the skill artifact.

Mitigation: Install and use the CLI only if its source and behavior are trusted in the target environment.

Risk: The Flatastic config stores a session token and household data locally.

Mitigation: Treat the config file as sensitive and restrict access to the local user account that needs Flatastic access.

Risk: Agent actions can change shared household records, including expenses, reminders, posts, and list items.

Mitigation: Require explicit user confirmation before destructive, financial, reminder, or message-posting operations.

## Reference(s):

- [Flatastic ClawHub skill page](https://clawhub.ai/david-schopf/skills/flatastic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline Flatastic CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the external flatastic CLI binary and a local Flatastic config containing a session token.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
