## Description:

Adds Cloudflare Zero Trust Access authentication in front of a VPS-hosted OpenClaw agent, including identity-provider setup, MFA policy guidance, service-token access for clients, multi-agent patterns, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to place Cloudflare Access in front of a VPS-hosted OpenClaw deployment, configure login and MFA policies, enable service-token access for programmatic clients, and troubleshoot access failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Service tokens act like long-lived credentials and can expose programmatic access if copied, committed, or left unrotated.

Mitigation: Use service tokens only for clients that need programmatic access, store secrets outside git, create per-client tokens, and rotate or revoke them promptly.

Risk: Rollback or bypass steps can remove the Cloudflare Access gate and leave only the OpenClaw authentication layers.

Mitigation: Review bypass changes before applying them and confirm the remaining OpenClaw token and pairing controls are appropriate for the deployment.

## Reference(s):

- [Service Tokens](references/service-tokens.md)
- [Cloudflare Access Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/cloudflare-access-vps)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell, JSON, JavaScript, and HTTP header examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; no hidden code or destructive behavior reported by security evidence.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
