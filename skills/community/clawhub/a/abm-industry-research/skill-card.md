## Description:

Orchestrates industry, keyword, search-intent, audience, content-gap, and competitor research using Ahrefs, Firecrawl, and Exa to produce a comprehensive intelligence brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mariokarras](https://clawhub.ai/user/mariokarras)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, SEO, and campaign-planning users use this skill to understand search demand, audience questions, keyword intent, content gaps, and competitor positioning before creating campaign briefs or content plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client names, seed keywords, competitor URLs, and research queries may be sent to external research services.

Mitigation: Review inputs for confidential or regulated information before running the skill, and use approved Ahrefs, Exa, and Firecrawl accounts or credentials.

Risk: The skill persists a synthesized research brief in the workspace.

Mitigation: Store the generated report only in approved workspaces and review retention or sharing requirements before distributing it.

Risk: Search, forum, and scraped-page findings can be stale, incomplete, or misleading.

Mitigation: Use the per-section research timestamps and review cited sources before relying on the brief for campaign or business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mariokarras/skills/abm-industry-research)
- [Publisher profile](https://clawhub.ai/user/mariokarras)
- [Ahrefs API v3 endpoint](https://api.ahrefs.com/v3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research brief with tables, dated sections, summarized findings, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local .agents/industry-research-{client}.md report; target artifact size is 3,000-5,000 words.]

## Skill Version(s):

1.0.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
