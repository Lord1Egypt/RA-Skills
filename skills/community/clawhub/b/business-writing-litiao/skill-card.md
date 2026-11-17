## Description:

Business Writing Litiao helps an agent produce business research reports, market analysis, company research, competitive analysis, user research, consulting analysis, and related business writing with Tavily-powered sourcing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and analysts use this skill to draft well-sourced business reports, market analyses, company research, competitive reviews, and strategic insights. It is suited for workflows that need current research, citations, Markdown tables, and Mermaid diagrams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs external research through Tavily and requires a Tavily API key.

Mitigation: Use it only when external search is appropriate, provide the API key through the expected environment variable, and avoid sending confidential query content to third-party search services unless approved.

Risk: Business reports can contain incorrect, outdated, or poorly supported claims if sources are not checked.

Mitigation: Review cited sources, cross-check important claims across multiple authoritative references, and verify that tables and Mermaid diagrams are based on real source data before publishing.

## Reference(s):

- [Business Writing Litiao on ClawHub](https://clawhub.ai/litiao1224/skills/business-writing-litiao)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with citations, tables, Mermaid diagrams, and inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY for Tavily-powered research.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
