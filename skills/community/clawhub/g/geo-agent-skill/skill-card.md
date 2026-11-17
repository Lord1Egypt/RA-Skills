## Description:

Diagnose a brand's visibility, recommendations, citations, competitor presence, factual accuracy, and content gaps in AI-assisted web search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuboboo](https://clawhub.ai/user/xuboboo)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, SEO/GEO practitioners, and developers use this skill to run traceable brand visibility audits across AI-assisted search, compare competitors, calculate metrics, and produce evidence-backed reports and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP tools can read outside the intended runs directory when given crafted run IDs.

Mitigation: Install only in trusted local environments, avoid untrusted run IDs, and do not expose the MCP server to untrusted clients until run_id path handling is fixed.

Risk: Live AI/search queries may send audit prompts and brand information to configured providers.

Mitigation: Use only approved providers and avoid submitting confidential brand data unless the provider path is approved for that data.

Risk: Optional alert channels may send alert details to configured email or webhook destinations.

Mitigation: Configure alert destinations explicitly and use only trusted recipients or webhook endpoints.

Risk: Scheduler command helpers may mishandle untrusted names or cron values until input validation and quoting are fixed.

Mitigation: Restrict scheduler configuration to trusted operators and pre-reviewed schedule names and cron expressions.

## Reference(s):

- [References Index](references/INDEX.md)
- [Workflow Specification](references/specification/workflow.md)
- [Security Specification](references/specification/security.md)
- [Metric Definitions](references/specification/metric-definitions.md)
- [Search Query Templates](references/specification/search-query-templates.md)
- [Search Signal Extraction](references/methodology/search-signal-extraction.md)
- [Multi-Engine Query](references/research/multi-engine-query.md)
- [llms.txt Specification](https://llmstxt.org/)
- [aio-surfaces](https://github.com/Janady/aio-surfaces)
- [geo-checklist](https://github.com/alexandrebrt14/geo-checklist)

## Skill Output:

**Output Type(s):** [text, markdown, json, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON reports, CSV exports, schema/configuration files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires validated brand inputs; live mode may call configured search or AI providers, while offline_import analyzes provided search results.]

## Skill Version(s):

0.1.3 (source: ClawHub release metadata; artifact frontmatter says 1.1.0 and artifact changelog says 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
