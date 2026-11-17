## Description:

Designs evaluation plans for LLM or AI features, covering task definition, datasets, metrics, rubrics, baselines, automated and human evaluation, pass bars, and regression gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI engineers, and product teams use this skill to create a repeatable evaluation plan before shipping or changing an LLM, prompt, model, agent, or AI feature.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Evaluation examples may include sensitive production logs or private customer data.

Mitigation: Use redacted or permissioned examples and avoid pasting sensitive data unless appropriate controls are in place.

Risk: Poorly calibrated LLM judges or vague rubrics can produce misleading evaluation decisions.

Mitigation: Calibrate judge behavior against human-labeled samples and require explicit rubric anchors before using scores for ship decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/ai-eval-plan)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/ai-eval-plan.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown evaluation plan]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task definition, dataset guidance, metrics and rubrics, baselines, pass thresholds, and regression gate criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
