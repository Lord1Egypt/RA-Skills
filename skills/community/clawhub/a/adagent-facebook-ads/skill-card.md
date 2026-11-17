## Description:

Manage Facebook/Meta Ads by creating campaigns, ad sets, and ads; researching audiences; monitoring performance; and checking relevant compliance status through AdAgent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External advertisers, marketing operators, and agents use this skill to manage Meta ad accounts through AdAgent, including campaign setup, targeting research, budget-related changes, performance reporting, and account compliance checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-like MCP connector links can grant access to the connected Meta ad account if shared or exposed.

Mitigation: Treat the MCP URL as a password, avoid sharing it, rotate the connector if exposed, and revoke Facebook authorization when access is no longer needed.

Risk: The skill can create, modify, pause, enable, and manage ads, campaigns, budgets, and targeting through a third-party service.

Mitigation: Connect only intended ad accounts and manually confirm budget, targeting, campaign creation, and activation changes before execution.

Risk: Persistent third-party OAuth access may continue until the user revokes it or the token expires.

Mitigation: Confirm how to revoke AdAgent's Facebook authorization and periodically review connected account permissions.

## Reference(s):

- [AdAgent product website](https://adagent.10xboost.org)
- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/adagent-facebook-ads)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown responses with structured ad account data, targeting options, workflow steps, and MCP tool-use guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed campaign, ad set, ad, targeting, budget, activation, and performance actions for user review.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
