## Description:

Helps users monitor AI provider quotas, subscription reset times, and API credit balances through a local dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthet1x](https://clawhub.ai/user/synthet1x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to configure a dashboard for tracking quotas, balances, and reset windows across AI providers and self-hosted gateways.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored provider credentials may be exposed to other local users.

Mitigation: Use read-only service tokens where possible, and restrict the configuration directory and file to the owner.

Risk: Remote dashboard access can reveal account telemetry.

Mitigation: Keep the dashboard local or add authentication before enabling port forwarding or a tunnel.

Risk: Browser session cookies give broader account access than dedicated API credentials.

Mitigation: Avoid browser session cookies; use official API keys or dedicated read-only service tokens.

Risk: Editing a credential pool while the collector runs can cause those changes to be overwritten.

Mitigation: Stop the collector before editing the pool, restart it, and confirm changes after a full collection cycle.

## Reference(s):

- [AI Quota Dashboard release](https://clawhub.ai/synthet1x/skills/ai-quota-dashboard)
- [Provider telemetry integration guide](artifact/references/api-reverse-engineering.md)
- [Credential security guide](artifact/references/security-cookie-guide.md)
- [Networking and deployment guide](artifact/references/networking-deployment.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with code blocks and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dashboard assets and normalized quota telemetry.]

## Skill Version(s):

1.2.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
