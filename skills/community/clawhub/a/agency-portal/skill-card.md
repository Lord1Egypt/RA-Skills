## Description:

Agency Portal helps agents operate a client self-service portal and administrator backend for tenant onboarding, login, plans, assets, reports, renewals, approvals, feedback, quotas, billing, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Agency operators and tenant-support teams use this skill to manage tenant onboarding, subscription changes, asset and report workflows, content approvals, feedback handling, quota and billing checks, patrols, and administrative follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad tenant, billing, publishing, approval, deletion, refund, payment, quota, subscription, suspension, and archiving actions may be available without enough documented safety gates.

Mitigation: Review before installation, use only with a trusted MCP server, and require explicit confirmations plus audit logging for destructive, billing, publishing, and account-status changes.

Risk: Admin tokens and portal secrets can authorize sensitive billing, tenant, publishing, and account changes.

Mitigation: Restrict admin tokens and configured secrets to authorized operators and rotate them according to the deployment's credential-management policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/agency-portal)
- [Agency portal reference data](artifact/scripts/agency_portal_reference.json)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Configuration]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and a configured agency-portal MCP server with the documented portal and admin environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
