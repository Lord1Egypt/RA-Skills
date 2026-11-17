## Description:

OpenClaw-native domain cascading that helps users reduce cost and latency with domain-aware model assignment, OpenClaw event handling, and setup commands such as /model cflow and optional /cascade stats.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saschabuehrle](https://clawhub.ai/user/saschabuehrle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure CascadeFlow as an OpenAI-compatible OpenClaw provider that routes requests through domain-aware drafter/verifier cascades for lower average cost and latency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users or agents to install and run a local service that handles credentials.

Mitigation: Review setup commands before execution, use a reviewed CascadeFlow version with trusted hashes or a lock file, and use limited-scope API keys with spending limits.

Risk: Sourcing untrusted environment files can expose or misuse provider credentials.

Mitigation: Review .env contents before loading them and keep separate test and production credentials.

Risk: Remote exposure of the service without appropriate protections can put chat and stats endpoints at risk.

Mitigation: Keep the service bound to localhost by default; if remote access is needed, use TLS or a reverse proxy with strong chat and stats tokens.

## Reference(s):

- [CascadeFlow publish pack](references/clawhub_publish_pack.md)
- [Market positioning for ClawHub](references/market_positioning.md)
- [CascadeFlow OpenClaw provider docs](https://github.com/lemony-ai/cascadeflow/blob/main/docs/guides/openclaw_provider.md)
- [CascadeFlow repository](https://github.com/lemony-ai/cascadeflow)
- [OpenClaw ClawHub docs](https://docs.openclaw.bot/guide/clawhub)
- [OpenClaw slash commands docs](https://docs.openclaw.bot/guide/faq/slash-commands)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, provider configuration, verification checks, and operational guidance for a local or TLS-protected CascadeFlow service.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
