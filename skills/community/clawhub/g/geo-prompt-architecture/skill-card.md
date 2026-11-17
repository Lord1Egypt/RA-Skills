## Description:

Generates, structures, scores, and audits topic-first GEO monitoring prompts from client business inputs, then turns AI visibility results into prompt and content optimization actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geo-seo](https://clawhub.ai/user/geo-seo)

### License/Terms of Use:

MIT-0

## Use Case:

GEO teams, agencies, operators, and software teams use this skill to build topic-first monitoring prompt systems across discovery, competitor comparison, and brand defense. It also supports prompt-set audits, structured scorecards, and recommendations that connect AI visibility results to content and asset optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some reference prompts document Chinese as the default language for analysis and structure, which may surprise users expecting English output.

Mitigation: Confirm the desired output language before client use and choose the English or Chinese generator reference accordingly.

Risk: Client workflows may involve sensitive analytics, internal documents, dashboards, or CRM context.

Mitigation: Use pasted public briefs or intentionally shared materials by default, and provide private client data only when the user explicitly wants the agent to use it.

## Reference(s):

- [Prompt Framework](references/prompt-framework.md)
- [Final Topic-First Generator Prompt](references/final-topic-first-generator-prompt.md)
- [Final Topic-First Generator Prompt (ZH)](references/final-topic-first-generator-prompt-zh.md)
- [Vertical Templates](references/vertical-templates.md)
- [Scoring Model](references/scoring-model.md)
- [Reverse Optimization](references/reverse-optimization.md)
- [Client Brief Schema](schemas/client-brief.schema.json)
- [Prompt Set Output Schema](schemas/prompt-set-output.schema.json)
- [Prompt Scorecard Schema](schemas/prompt-scorecard.schema.json)
- [ClawHub Skill Page](https://clawhub.ai/geo-seo/skills/geo-prompt-architecture)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, configuration, guidance]

**Output Format:** [Markdown, tables, or JSON matching the bundled schemas]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured topic maps, prompt sets, scorecards, audits, and optimization recommendations; no executable commands are required.]

## Skill Version(s):

0.1.3 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
