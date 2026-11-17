## Description:

Complete toolkit for the Cesto platform; covers public basket analytics, authenticated basket creation, portfolio simulation, and market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lakshyagarg26](https://clawhub.ai/user/lakshyagarg26)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Cesto baskets, analyze token and basket performance, create Cesto Labs baskets after authentication, and simulate portfolio performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Cesto access and refresh tokens on disk for authenticated flows.

Mitigation: Use the skill only in trusted environments, revoke or rotate Cesto credentials after testing, and prefer a secure credential store before production use.

Risk: Authenticated flows can create public Cesto Labs baskets or run portfolio simulations using the user's account.

Mitigation: Require an explicit user preview and confirmation before any publishing action, and verify the final title, description, and allocations before submission.

Risk: Public basket data may include unpublished baskets in user-facing output.

Mitigation: Filter user-facing basket lists and analytics to published baskets unless the user explicitly asks for unpublished or internal records and has authority to view them.

Risk: URL origin validation and plaintext auth.json behavior were flagged by the security evidence.

Mitigation: Review and fix exact origin matching and token storage before approving broad or unattended use.

## Reference(s):

- [Cesto API Reference](references/api-reference.md)
- [Cesto App](https://app.cesto.co)
- [Cesto Backend API](https://backend.cesto.co)
- [ClawHub Skill Page](https://clawhub.ai/lakshyagarg26/skills/cesto-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with tables and inline shell commands; helper scripts return JSON for the agent to summarize.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Cesto basket links, performance summaries, token allocation tables, and authenticated publishing or simulation results.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
