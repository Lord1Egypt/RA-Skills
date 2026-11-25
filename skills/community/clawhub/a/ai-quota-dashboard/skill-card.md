## Description:

Real-time multi-provider AI quota dashboard: model limits, token balances, subscription reset timers. Secure local token management (owner-only files, domain pinning, zero argv leakage) and a deployment/telemetry guide. Trigger phrases: quota dashboard, AI limits, token balance, subscription resets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synthet1x](https://clawhub.ai/user/synthet1x)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use the dashboard to monitor quotas, balances, and reset times across provider APIs and self-hosted gateways, and to configure local collection and deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The collector handles provider access tokens, and accidental exposure could compromise accounts.

Mitigation: Use official, least-privilege API keys or read-only service tokens; store them in owner-only configuration files and never pass them as command-line arguments.

Risk: An internet-accessible dashboard could expose private quota and account telemetry.

Mitigation: Keep access local or behind a VPN, or require authentication and restrict permitted source addresses before exposing it remotely.

Risk: The benign security verdict has medium confidence because scan coverage was partial.

Mitigation: Review the unscanned or limited components and the skill’s credential and network behavior before installation.

## Reference(s):

- [Credential isolation and safe token management](artifact/references/security-cookie-guide.md)
- [Networking and deployment guide](artifact/references/networking-deployment.md)
- [Custom and self-hosted provider telemetry guide](artifact/references/api-reverse-engineering.md)
- [ClawHub release page](https://clawhub.ai/synthet1x/skills/ai-quota-dashboard)

## Skill Output:

**Output Type(s):** [Files, Code, Configuration instructions, Shell commands, Guidance]

**Output Format:** [HTML dashboard, Python collector, JSON configuration and telemetry, and Markdown deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local quota and subscription telemetry collected from configured provider APIs or self-hosted gateways.]

## Skill Version(s):

1.2.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
