## Description:

AGI Farm is an OpenClaw skill that bootstraps a multi-agent AI team with generated workspaces, communication files, cron automation, optional GitHub export, and a React/SSE operations dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oabdelmaksoud](https://clawhub.ai/user/oabdelmaksoud)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use AGI Farm to create and manage a configurable multi-agent workspace for software, trading, research, general, or custom domains. It supports setup, status checks, workspace rebuilds, bundle export, dashboard monitoring, and task dispatch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard exposes powerful workflow controls and uses broad CORS behavior.

Mitigation: Bind the dashboard to localhost only, add authentication before shared use, remove wildcard CORS, and avoid exposing port 8080.

Risk: The skill creates agents, writes OpenClaw workspace files, and registers recurring automation.

Mitigation: Review generated files and cron registrations before enabling automated runs, and use dry-run modes where available.

Risk: The optional export flow may push a public GitHub repository.

Mitigation: Review the bundle contents, repository visibility, authentication state, and remote target before running export or setup with GitHub creation enabled.

Risk: Framework integrations and dashboard dependencies can drift over time.

Mitigation: Pin or vendor framework integrations where possible and update dashboard dependencies before operational use.

## Reference(s):

- [Dashboard Reference](references/dashboard.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands plus generated JSON, Markdown, Python, and dashboard files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local OpenClaw workspace; can register recurring automation and run a local dashboard.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
