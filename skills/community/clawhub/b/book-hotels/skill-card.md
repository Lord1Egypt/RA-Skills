## Description:

Uses the RollingGo CLI to search hotels, filter results, retrieve hotel tags, and get room pricing for destination, date, star-rating, budget, tag, and distance queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longcreat](https://clawhub.ai/user/longcreat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and travel-support agents use this skill to find candidate hotels, compare current structured hotel data, inspect room prices, and provide booking links or hotel-detail links when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to run the latest remote RollingGo CLI package, which can change between executions.

Mitigation: Prefer a pinned and reviewed RollingGo package version, avoid global installs, and re-scan the skill before deployment.

Risk: API-key handling examples include command-line and environment-variable patterns that can expose credentials if copied carelessly.

Mitigation: Inject only the RollingGo API key through scoped host or sandbox environment configuration and avoid passing real API keys directly on the command line.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/longcreat/skills/book-hotels)
- [Publisher profile](https://clawhub.ai/user/longcreat)
- [RollingGo homepage](https://rollinggo.store)
- [RollingGo API key application](https://rollinggo.store/apply)
- [RollingGo NPX reference](references/rollinggo-npx.md)
- [RollingGo UV reference](references/rollinggo-uv.md)
- [Claw host environment reference](references/claw-host-env.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The RollingGo CLI writes result data to stdout, defaults to JSON, writes errors to stderr, and can return booking URLs or hotel-detail links.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
