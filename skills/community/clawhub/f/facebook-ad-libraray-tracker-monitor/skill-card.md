## Description:

Monitor Facebook ads and advertisers with PPSPY, including tracking tasks, ad activity over time, landing pages, products, and monitoring groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, ecommerce, and competitive intelligence teams use this skill through an agent to create and manage PPSPY monitoring tasks for Facebook advertisers, then review ad activity, landing pages, products, and trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party PPSPY npm package and a PPSPY account API key.

Mitigation: Install only if you trust PPSPY and ppspy-mcp-server@1.0.1; store PPSPY_API_KEY as a secret and rotate it if package or account activity becomes untrusted.

Risk: Some PPSPY actions consume monitoring quota or credits.

Mitigation: Monitor account credit usage and review task-creation actions before execution.

## Reference(s):

- [PPSPY product website](https://www.ppspy.com)
- [PPSPY API website](https://api.ppspy.com/)
- [ClawHub skill page](https://clawhub.ai/fanyanggod/skills/facebook-ad-libraray-tracker-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool names, configuration snippets, and suggested agent actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PPSPY_API_KEY and the ppspy-mcp-server@1.0.1 npm package; some actions consume PPSPY account quota.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
