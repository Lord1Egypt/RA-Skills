## Description:

Find and monitor open roles on supported company career sites, with filters for title, location, seniority, salary, and posting date.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jordan-belfort-ai](https://clawhub.ai/user/jordan-belfort-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, recruiters, and talent teams can use the skill to search supported employers' career pages and monitor newly posted roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company lists and search filters are processed by Apify and the author's community Actors, and returned jobs incur a per-job charge.

Mitigation: Review current pricing, set a result cap, and consider how the selected providers handle submitted company lists and filters.

Risk: The first monitoring run returns all current matching jobs; remote Actor code and live behavior have not been independently verified.

Mitigation: Enable recurring watches only when wanted, cap and review the initial results, and check subsequent results.

## Reference(s):

- [Actor index](references/actor-index.md)
- [Cost guardrails and troubleshooting](references/gotchas.md)
- [Apify schedules](https://docs.apify.com/platform/schedules)
- [Apify MCP integration](https://docs.apify.com/platform/integrations/mcp)
- [Apify MCP client](https://github.com/apify/mcpc)

## Skill Output:

**Output Type(s):** [API Calls, Structured data, Shell commands, Guidance]

**Output Format:** [JSON job records with a concise Markdown summary and dataset link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized job listings with optional filters and monitoring for newly seen jobs.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
