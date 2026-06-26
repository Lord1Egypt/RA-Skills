## Description: <br>
Use when the user wants to generate, structure, score, or audit GEO monitoring prompts for a client. Trigger when building topic-first prompt sets from a website, brand, market, customer, product lines or inferred topics, and competitors; when balancing non-brand, comparison, and brand-defense prompts; or when turning AI visibility monitoring results into prompt and content optimization actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[GEO-SEO](https://clawhub.ai/user/GEO-SEO) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External GEO software teams, agencies, and marketing operators use this skill to turn client briefs, websites, product lines, competitors, and monitoring results into topic-first GEO prompt sets and optimization recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Client briefs, screenshots, exports, monitoring results, or website content may contain sensitive business information. <br>
Mitigation: Provide only the materials the agent is intended to use, and avoid supplying private analytics, CRM, dashboard, or credential-backed data unless it is necessary and authorized. <br>
Risk: Prompt-generation outputs can include inferred product lines, topics, competitors, markets, or optimization actions that may be wrong for the client. <br>
Mitigation: Review inferred fields before using the prompt set for monitoring, reporting, or content planning. <br>
Risk: Some reference prompts may produce Chinese output structure when that is not desired. <br>
Mitigation: State the required output language explicitly when invoking the skill. <br>


## Reference(s): <br>
- [Prompt Framework](references/prompt-framework.md) <br>
- [Vertical Templates](references/vertical-templates.md) <br>
- [Reverse Optimization](references/reverse-optimization.md) <br>
- [Scoring Model](references/scoring-model.md) <br>
- [Final Topic-First Generator Prompt](references/final-topic-first-generator-prompt.md) <br>
- [Final Topic-First Generator Prompt (ZH)](references/final-topic-first-generator-prompt-zh.md) <br>
- [Client Brief Schema](schemas/client-brief.schema.json) <br>
- [Prompt Set Output Schema](schemas/prompt-set-output.schema.json) <br>
- [Prompt Scorecard Schema](schemas/prompt-scorecard.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance, Configuration] <br>
**Output Format:** [Markdown tables and structured JSON-compatible prompt, topic, scorecard, and recommendation outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default generation targets five topics and fifty prompts, with topic-first grouping across non-brand discovery, competitor comparison, and brand-defense layers.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
