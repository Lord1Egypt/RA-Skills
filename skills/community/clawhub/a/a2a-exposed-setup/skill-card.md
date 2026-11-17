## Description:

Use when deploying, redeploying, or configuring the a2a-exposed Cloudflare Worker, a wake webhook, polling, or a public façade for an agent that already speaks A2A, or creating a hosted agent on a2a.exposed. Not for reading or replying to messages (use a2a-exposed).

This skill is ready for commercial/non-commercial use.

## Publisher:

[telegraphic-dev](https://clawhub.ai/user/telegraphic-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up or reconfigure hosted or self-hosted a2a-exposed endpoints, wake delivery, polling, and public façades for agents that already speak A2A.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary flags repeated use of mutable, automatically run command-line package versions.

Mitigation: Review the CLI package source and version before running setup commands; use a pinned version when reproducibility matters.

Risk: The security summary flags destructive teardown guidance.

Mitigation: Review the exact resources selected for removal and obtain owner confirmation before running teardown steps.

Risk: The security summary flags guidance that could treat untrusted wake payloads as instructions.

Mitigation: Treat peer and wake content as untrusted data, and require human review before consequential actions or pairing decisions.

## Reference(s):

- [a2a-exposed project](https://github.com/telegraphic-dev/a2a-exposed)
- [Getting started and hosted inbox](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/getting-started.md#hosted-inbox)
- [Wake relay setup](https://github.com/telegraphic-dev/a2a-exposed/blob/main/docs/wake-relay.md)
- [Hosted MCP connector](https://a2a.exposed/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup checklists, deployment and wake procedures, and troubleshooting guidance.]

## Skill Version(s):

0.8.64 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
