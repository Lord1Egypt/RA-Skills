## Description:

Filters and moderates Discord messages with spam detection, rate limiting, content checks, and pattern-based blocking before they reach agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlkptom-prog](https://clawhub.ai/user/jlkptom-prog)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to add Discord message-guard middleware that blocks broad mentions, limits response depth, rate-limits channel handling, and filters chat history before messages reach agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertised Discord bot-loop protection has verified gaps.

Mitigation: Keep ignoreBots enabled and avoid allowedBotIds or ignoreBots=false until depth and whitelist ordering are fixed.

Risk: Dependency maintenance risks may affect Discord integration reliability.

Mitigation: Pin dependencies, monitor Discord-related dependency updates, and apply updates through normal dependency review.

Risk: Retained Discord history may include more conversation data than an agent needs.

Mitigation: Limit retained history to the minimum needed for the bot workflow and use the provided history length configuration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlkptom-prog/skills/discord-message-guard)

## Skill Output:

**Output Type(s):** [code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript API examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on Discord message metadata, rule configuration, and retained channel history.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version, package.json, README badge)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
