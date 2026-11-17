## Description:

AI 产品经理教练，通过引导式对话帮助 PM 完成从痛点分析到 PRD 输出的 AI 产品设计，并在关键节点要求 PM 做出选择。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lijinhongucl-pixel](https://clawhub.ai/user/lijinhongucl-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers and product teams use this Chinese-language coaching agent to work through AI product design decisions, including pain point validation, AI suitability, capability boundaries, confidence thresholds, hallucination handling, and PRD assembly. The agent guides discussion and records choices without replacing the PM's decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms such as AI product, product design, or PRD may activate the workflow in conversations where the user expected a narrower response.

Mitigation: Invoke the skill explicitly when possible and confirm that the user wants a guided AI product-design coaching workflow before proceeding.

Risk: The skill content is Chinese-language, which can limit usability or review quality for non-Chinese-speaking users or reviewers.

Mitigation: Use it for Chinese-language PM coaching contexts, or require bilingual review before using outputs in multilingual or English-only teams.

Risk: The agent produces product-management guidance and PRD drafts that could be mistaken for final product decisions.

Mitigation: Keep the documented decision checkpoints in place and require PM confirmation before treating generated PRD sections, thresholds, or risk boundaries as final.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lijinhongucl-pixel/skills/ai-pm-prd-suite)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational text with Markdown product-management artifacts and occasional JSON-style structured assessments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may generate PRD sections, AI capability boundary statements, confidence mechanisms, hallucination response plans, and decision summaries for user confirmation.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
