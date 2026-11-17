## Description:

GEO operations assistant for helping operators improve how content is cited by generative search engines through keyword expansion, citation-source analysis, content optimization, publishing strategy, and validation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ludiansheng](https://clawhub.ai/user/ludiansheng)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, marketers, and content teams use this skill to evaluate and improve content for generative engine optimization. It supports quick citation-potential checks and a full workflow covering semantic analysis, keyword expansion, source authority assessment, content drafting, publishing strategy, validation, and follow-up optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional webpage fetcher can retrieve arbitrary URLs and may expose agent environments to unsafe outbound network access.

Mitigation: Prefer pasted webpage text; when URL fetching is needed, run it only in an environment that blocks private networks, metadata services, and other sensitive internal destinations.

Risk: Generated reports may contain confidential prompts, answers, client data, screenshots, or unpublished content.

Mitigation: Redact sensitive business and personal data before including it in reports or sharing generated outputs.

Risk: Citation-potential predictions and simulated model answers can be misleading if treated as guaranteed outcomes.

Mitigation: Validate recommendations manually across the target models and track actual citation behavior before using the results for business decisions.

## Reference(s):

- [Skill release page](https://clawhub.ai/ludiansheng/skills/geo-operation-assistant)
- [Quick GEO Detection Guide](references/quick_guide.md)
- [GEO Knowledge Base](references/geo_knowledge_base.md)
- [Keyword Expansion Strategy](references/keyword_strategy.md)
- [Authority Assessment Criteria](references/authority_criteria.md)
- [Content Template Library](references/content_template.md)
- [GEO Validation Report Template](assets/report_template.md)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown prose, tables, checklists, report templates, optional JSON from helper scripts, and optional shell commands for local scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include keyword tables, authority assessments, content drafts, publishing plans, validation reports, and optimization recommendations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
