## Description: <br>
Adds Cloudflare Zero Trust Access authentication in front of a VPS-hosted OpenClaw agent domain, including browser login, MFA policies, service tokens for native or API clients, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to place Cloudflare Access in front of OpenClaw agents hosted on a VPS, define identity policies, configure service-token access for non-browser clients, and troubleshoot deployment issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security-sensitive rollback, localhost bypass, or exposure guidance could weaken the deployment if left in place after troubleshooting. <br>
Mitigation: Treat bypass and rollback steps as temporary, keep the OpenClaw service bound to loopback unless intentionally exposed, and restore Cloudflare Access controls after diagnosis. <br>
Risk: Service tokens can function like long-lived credentials if shared, committed, or not rotated. <br>
Mitigation: Use scoped tokens per client or device, prefer expiring and rotated tokens, store secrets outside source control, and revoke lost or unused tokens. <br>


## Reference(s): <br>
- [Service Tokens - Programmatic Access Through Cloudflare Access](references/service-tokens.md) <br>
- [Cloudflare Access Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with tables, checklists, configuration examples, and inline code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
