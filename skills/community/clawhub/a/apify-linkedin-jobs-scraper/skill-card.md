## Description:

Search public LinkedIn job postings through Apify and return structured listings with job, salary, recruiter, and optional company details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harshmaur](https://clawhub.ai/user/harshmaur)

### License/Terms of Use:

MIT-0

## Use Case:

Job seekers, recruiters, and analysts can search public LinkedIn listings and organize hiring, salary, recruiter, and company information. It supports keyword and search-URL queries, with optional scheduled alerts when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid Actor runs and cloud storage of searches and results can create costs or data-handling concerns.

Mitigation: Check current pricing and result limits before running; review storage destinations and recurring costs before enabling alerts.

Risk: The inspected skill files do not establish the security of the remotely maintained Actor.

Mitigation: Treat the Actor as a separate service and review its current behavior before providing credentials or running searches.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/harshmaur/skills/apify-linkedin-jobs-scraper)
- [Apify MCP integration documentation](https://docs.apify.com/platform/integrations/mcp)
- [Apify MCP server for this Actor](https://mcp.apify.com/?tools=harshmaur/linkedin-jobs-scraper)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Text]

**Output Format:** [Structured job records in an Apify dataset, with optional Markdown summaries or tables and CSV export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fields may be unavailable; applicant counts are capped, results are bounded, and some workplace, job-type, and seniority filters are approximate.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
