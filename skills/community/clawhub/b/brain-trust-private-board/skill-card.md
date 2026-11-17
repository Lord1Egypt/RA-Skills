## Description:

智囊团式私董会多专家协作分析框架，支持2-5位专家私董会式动态讨论、正反辩论、红队审查、方案对比和综合决策判断。

This skill is ready for commercial/non-commercial use.

## Publisher:

[e2e5g](https://clawhub.ai/user/e2e5g)

### License/Terms of Use:

exclusive

## Use Case:

External users use this skill for complex judgment tasks such as strategy decisions, product direction, business plan review, management questions, learning plans, research analysis, critiques, red-team reviews, and synthesis. It helps structure a 2-5 expert private-board style discussion that compares perspectives and turns them into a practical recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for a wide range of strategy, product, management, learning, and research prompts.

Mitigation: Deploy it for complex judgment tasks where expert framing adds value, and route ordinary fact questions, simple rewrites, translation, and direct advice requests to simpler handling.

Risk: Expert-style framing can make analysis sound more authoritative than the evidence supports.

Mitigation: Treat expert views as reasoning frameworks rather than facts, and verify facts, data, dates, policies, and source claims through the normal evidence-checking process.

Risk: The skill's Chinese-language behavior may not be obvious to multilingual users.

Mitigation: Confirm the desired response language and output style when deploying it in multilingual workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/e2e5g/skills/brain-trust-private-board)
- [Call patterns](references/call-patterns.md)
- [Deliverable templates](references/deliverable-templates.md)
- [Expert frameworks](references/expert-frameworks.md)
- [Expert selection guide](references/expert-selection.md)
- [High-frequency use cases](references/high-frequency-use-cases.md)
- [Output modes and templates](references/output-modes.md)
- [Output style templates](references/output-style-templates.md)
- [Quality guardrails](references/quality-guardrails.md)
- [Skill, prompt, and workflow review](references/skill-prompt-review.md)
- [Task recipes](references/task-recipes.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or natural-language text, with JSON only when the caller asks for machine-readable output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language expert-panel analysis with optional structured fields for mode, selected experts, problem frame, discussion flow, synthesis, recommended path, next actions, confidence, and missing information.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
