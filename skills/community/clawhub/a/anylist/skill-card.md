## Description:

Manage grocery and shopping lists via AnyList. Use when user asks about shopping lists, groceries, or adding/checking off items to buy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mjrussell](https://clawhub.ai/user/mjrussell)

### License/Terms of Use:


## Use Case:

External users and personal productivity agents use this skill to inspect, add, check, uncheck, remove, and clear items in AnyList grocery or shopping lists through the AnyList CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a global npm installation of anylist-cli.

Mitigation: Verify the npm package source before installation and consider pinning a reviewed anylist-cli version.

Risk: AnyList account credentials may be exposed through environment variables or shell history.

Mitigation: Prefer interactive authentication when practical and avoid storing passwords in shared shell history or committed files.

Risk: Delete-style commands can remove items or clear checked items from a list.

Mitigation: Ask the agent to confirm before running remove or clear operations.

## Reference(s):

- [AnyList homepage](https://www.anylist.com)
- [ClawHub skill page](https://clawhub.ai/mjrussell/skills/anylist)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the anylist CLI and supports JSON output for list and item inspection commands.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
