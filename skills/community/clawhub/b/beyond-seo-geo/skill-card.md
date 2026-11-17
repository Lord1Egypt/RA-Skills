## Description:

Use for SEO audits, AEO/GEO strategy, local SEO, backlink review, competitor research, keyword mapping, Apify/native scraping workflows, and client-ready SEO reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beyondtahir](https://clawhub.ai/user/beyondtahir)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and SEO teams use this skill to run evidence-based SEO, AEO/GEO, local SEO, backlink, competitor, keyword, and reporting workflows. It supports live data collection through Apify or native tools when available and falls back to uploaded-file or advisory analysis when live data is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional Apify, native scraping, and scheduled monitoring workflows may make broad network or third-party requests.

Mitigation: Review before installation, use a scoped Apify token, and approve each external crawl, scrape, connector run, or scheduled monitor.

Risk: Live account access or exported analytics/search data can expose sensitive business or customer information.

Mitigation: Prefer redacted exports, avoid live account access unless needed, and never store or repeat API tokens in skill files, reports, templates, manifests, or logs.

Risk: The optional sitemap extractor can be pointed at untrusted URLs.

Mitigation: Do not run the extractor against untrusted URLs without URL validation and private-network protections.

Risk: SEO, backlink, traffic, ranking, and AI-search visibility conclusions can be misleading when data is missing or based on directional third-party sources.

Mitigation: Label evidence as confirmed, directional, estimated, or not verified, and require exports or reliable data sources before presenting metrics as facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/beyondtahir/skills/beyond-seo-geo)
- [README](artifact/README.md)
- [AI-Friendly SEO Master Workflow](artifact/aeo-geo/ai-friendly-seo-master-workflow.md)
- [Apify-First Operating Policy](artifact/integrations/apify-first-operating-policy.md)
- [Release Notes](artifact/RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, checklists, plans, templates, and optional shell or Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should label missing or estimated data and avoid claims of rankings, traffic, backlinks, or AI citations unless verified from available evidence.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
