## Description:

Drive Databar MCP: leads, marketing intel, tables, flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dennisrongo](https://clawhub.ai/user/dennisrongo)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to run Databar MCP workflows for lead enrichment, marketing intelligence, web data pulls, table pipelines, flows, and CRM exports with explicit price checks before paid operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Databar operations can spend workspace credits on enrichment, waterfall, table, and export workflows.

Mitigation: Check balance and provider price before each run, estimate the full workflow cost, and report the credit delta after completion.

Risk: Lead generation and enrichment workflows may process personal contact data or data governed by platform terms and privacy law.

Mitigation: Use the skill only for lawful, permitted data workflows and review contact-data handling, outreach, and redistribution obligations before export or reuse.

Risk: CRM exports, scheduled sources, and table or flow deletion operations can have lasting effects.

Mitigation: Require explicit user confirmation before exports, schedules, or destructive table, row, column, folder, and flow operations.

## Reference(s):

- [Databar MCP documentation](https://docs.databar.ai/mcp-server)
- [Databar](https://databar.ai/)
- [Databar hosted MCP endpoint](https://mcp.databar.ai/mcp)
- [ClawHub listing](https://clawhub.ai/dennisrongo/databar-mcp)
- [Databar Recipes](references/recipes.md)
- [Databar Recipes - Marketing, SEO & Social](references/recipes-marketing-social.md)
- [Databar Recipes - Job Search, Recruiting & Research](references/recipes-people-research.md)
- [Databar Recipes - Finance, Apps & Web Traffic](references/recipes-finance-app.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with tool-call guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Databar task IDs, credit estimates, enrichment results, table workflow steps, and export guidance.]

## Skill Version(s):

0.2.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
