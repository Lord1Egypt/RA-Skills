## Description:

Manage Google Ads campaigns: create, monitor, pause, and optimize search ads, keyword research, performance reporting, and account workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and ad operators use this skill to manage Google Ads accounts through AdAgent, including account listing, keyword research, campaign creation, performance reporting, and campaign pause or enable actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP Connector link functions like a secret and may allow access to Google Ads account data and actions if exposed.

Mitigation: Keep the connector link private, avoid committing or sharing it, and revoke or regenerate access immediately if it is exposed.

Risk: The connected service can create campaigns, change budgets, enable or pause campaigns, and read performance data.

Mitigation: Verify OAuth permissions and confirm the target account, budget, geography, language, final URL, and activation state before campaign creation or enablement.

Risk: Installation depends on trust in the third-party AdAgent service for Google Ads account access.

Mitigation: Install only after reviewing the service and confirming it is acceptable for the user's Google Ads account and organizational policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snoopyrain/skills/adagent-google-ads)
- [snoopyrain publisher profile](https://clawhub.ai/user/snoopyrain)
- [AdAgent homepage](https://adagent.10xboost.org)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, API calls]

**Output Format:** [Markdown with tool-call guidance and tabular summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include campaign IDs, performance metrics, keyword suggestions, account lists, and setup instructions for an MCP Connector link.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
