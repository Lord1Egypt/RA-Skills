## Description:

Routes text and image tasks across Chinese model providers with task-aware model selection, cost tracking, and local evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fyniujin](https://clawhub.ai/user/fyniujin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use one command-line interface to route work across model providers, compare cost and capability, and review local evaluation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks this release suspicious, citing mismatches between advertised features and behavior plus unexpected network and data-retention risks; six referenced paths were unresolved.

Mitigation: Review the scanner findings and unresolved paths before installation, and proceed only if the reported behavior is acceptable.

Risk: Prompts may be sent to selected model providers; optional webhook alerts, possible model downloads, and local caching add data-handling considerations.

Mitigation: Send only prompts approved for the selected providers, configure webhook destinations deliberately, review download sources, and disable or clear caching for sensitive tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fyniujin/skills/cn-llm-router)
- [SkillHub project page](https://skillhub.cn/skill/cn-llm-router)
- [Routing rules](references/routing-rules.md)
- [Model registry](references/models.yaml)
- [Local evaluation suite](references/eval_suite.json)

## Skill Output:

**Output Type(s):** [Text, Code, JSON, Reports, Guidance]

**Output Format:** [Provider responses as text or JSON, with Markdown or HTML reports and SVG evaluation charts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected provider and model; streaming is supported where available.]

## Skill Version(s):

2.9.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
