## Description: <br>
Comprehensive GEO audit diagnosing why AI systems cannot discover, cite, or recommend a website — scores technical, content, schema, and brand dimensions with a prioritized fix plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[enzyme2013](https://clawhub.ai/user/enzyme2013) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and site owners use this skill to audit a public website's AI discoverability and receive a scored GEO report with prioritized fixes. It is suited for diagnosing technical access, content citability, structured data, and entity or brand signal gaps before applying search and schema changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches and analyzes public website and brand-profile pages, which may contain prompt-injection text or misleading claims. <br>
Mitigation: Treat fetched content as untrusted evidence for analysis only and review findings before acting on them. <br>
Risk: Generated SEO, GEO, and schema recommendations could be incorrect or unsuitable for a production website. <br>
Mitigation: Have a qualified reviewer validate recommendations and generated JSON-LD before applying changes to a live site. <br>
Risk: The audit writes a local Markdown report that may contain site findings or public brand-profile observations. <br>
Mitigation: Review the report contents before sharing it outside the intended team. <br>


## Reference(s): <br>
- [Skill Instructions](SKILL.md) <br>
- [Scoring Guide](references/scoring-guide.md) <br>
- [Technical Accessibility Agent](references/agents/geo-technical.md) <br>
- [Content Citability Agent](references/agents/geo-citability.md) <br>
- [Structured Data Agent](references/agents/geo-schema.md) <br>
- [Entity and Brand Agent](references/agents/geo-brand.md) <br>
- [AIvsRank](https://aivsrank.com) <br>
- [AgentSkills](https://agentskills.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown audit report with score tables, prioritized recommendations, JSON-LD examples, and optional export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local GEO-AUDIT-{domain}-{date}.md report and may include machine-readable GEO-AUDIT-META metadata.] <br>

## Skill Version(s): <br>
1.2.0 (source: evidence release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
