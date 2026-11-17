## Description:

域名DNS管理专业版 helps operations teams and enterprises coordinate domain and DNS assets across bulk domain onboarding, multi-provider DNS management, Worker routing, audit logging, health checks, rollback, DNSSEC, and multi-account workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, site reliability engineers, MSP operators, and domain operations teams use this skill to plan and execute DNS record, nameserver, redirect, audit, rollback, monitoring, and provider migration workflows for managed domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: DNS, nameserver, redirect, DNSSEC, Worker, rollback, cron, or bulk operations can cause outages or traffic misrouting if applied to the wrong domain or account.

Mitigation: Require a preview and explicit human confirmation before executing changes, verify the active account and domain list, and test on non-production domains before production rollout.

Risk: Broad API credentials could allow unintended changes across multiple providers or customer accounts.

Mitigation: Use least-privilege provider tokens, isolate credentials per account or customer, and avoid storing secrets in skill files or plain configuration.

Risk: Batch execution can amplify a mistaken record, nameserver, redirect, or DNSSEC change across many domains.

Mitigation: Run small batches first, keep checkpoints and pre-change snapshots, review generated reports, and confirm rollback procedures before scaling up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/domain-dns-manager-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, YAML configuration examples, and JSON result structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe high-impact DNS, nameserver, redirect, DNSSEC, Worker, audit, rollback, cron, and bulk-operation steps that require operator review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
