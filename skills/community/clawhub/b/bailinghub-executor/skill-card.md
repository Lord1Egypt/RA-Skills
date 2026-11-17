## Description:

Connects OpenClaw to a self-hosted BailingHub agent governance control plane as an outbound executor for governed business actions, human approval, audit trails, and secure tool execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bailinghub](https://clawhub.ai/user/bailinghub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect a local OpenClaw agent to a self-hosted BailingHub target so governed jobs can be claimed, processed, verified, and reported without opening an inbound executor port.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: This machine will process jobs from the configured BailingHub target and pass task text to the selected OpenClaw runtime and model provider.

Mitigation: Install only for intended targets, begin with BAILING_RUN_ONCE=1 on non-sensitive test data, and confirm the task data path is approved for the chosen model provider.

Risk: Executor tokens or additional provider variables could be exposed if the host or process environment is configured too broadly.

Mitigation: Use a target-scoped token, run under a dedicated non-root account, keep credentials out of command lines and logs, and limit OPENCLAW_FORWARD_ENV to the exact variables OpenClaw needs.

Risk: BailingHub approval and audit records do not replace business-system authorization or host hardening.

Mitigation: Keep final authority in the business system, maintain independent audit trails where required, rotate secrets after suspected exposure, and test revocation, shutdown, stale results, and timeouts before production use.

## Reference(s):

- [Setup and verification](references/setup.md)
- [Security boundary](references/security.md)
- [BailingHub OpenClaw Skill](https://github.com/bailinghub/bailinghub-openclaw-skill)
- [BailingHub Agent Governance Executor](https://clawhub.ai/bailinghub/skills/bailinghub-executor)
- [BailingHub Publisher Profile](https://clawhub.ai/user/bailinghub)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup, verification, and operational reporting while instructing agents not to expose credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
