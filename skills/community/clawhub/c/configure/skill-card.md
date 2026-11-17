## Description:

Set up a Discord channel by saving the bot token and reviewing the access policy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure a Discord bot token, inspect who can reach the assistant through Discord, and move access from temporary pairing to a locked allowlist.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores a Discord bot token locally in ~/.claude/channels/discord/.env.

Mitigation: Install only in an agent environment trusted to manage the token, keep the machine and account protected, and rotate the token if it is exposed.

Risk: Pairing mode can allow additional Discord users to request access before the allowlist is locked.

Mitigation: Use pairing only to capture intended user IDs, then switch the policy to allowlist once the expected users are present.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eohmig/skills/configure)
- [Publisher profile](https://clawhub.ai/user/eohmig)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration status guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write, update, or clear a local Discord bot token configuration file when invoked with token-management arguments.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
