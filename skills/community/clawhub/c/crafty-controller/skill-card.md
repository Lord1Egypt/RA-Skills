## Description:

Crafty Controller helps agents manage Minecraft servers through a Crafty Controller REST API, including server actions, console commands, stats, backups, schedules, files, users, and roles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zdstudios](https://clawhub.ai/user/zdstudios)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and server operators use this skill to generate guidance, Python helper code, shell setup commands, and API call patterns for administering Crafty Controller Minecraft server panels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The examples disable TLS certificate verification while using bearer API keys.

Mitigation: Enable certificate verification with a trusted CA bundle before using the generated helpers against real Crafty Controller instances.

Risk: The skill covers destructive and account-changing administrative actions such as deleting servers, deleting backups, changing users, and assigning roles.

Mitigation: Use a dedicated least-privilege API key and require explicit operator confirmation before destructive, permission-changing, or account-changing calls.

Risk: API keys can be exposed if copied into shared source or chat transcripts.

Mitigation: Store Crafty Controller API keys in a secrets manager or local environment variables, and avoid committing credentials with generated helper code.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zdstudios/skills/crafty-controller)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Python, shell, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include REST API helper functions and operational recommendations for Crafty Controller instances.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
