## Description:

Designs scoring rubrics and LLM-as-judge prompts for evaluating AI feature outputs, including weighted dimensions, concrete 1-5 anchors, labelling guidance, and judge reliability notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and evaluators use this skill to define observable quality dimensions, anchored scoring rubrics, and ready-to-run LLM-as-judge prompts for AI output evaluation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rubric calibration may involve sample AI outputs or quality requirements that contain confidential information.

Mitigation: Review and redact confidential examples before using them in judge prompts or sharing them with an AI judge workflow.

Risk: Poorly calibrated judge prompts can produce misleading evaluation scores.

Mitigation: Calibrate the rubric against good and weak samples, sample repeated judge runs, and spot-check judge scores against human labels before relying on rankings.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mohitagw15856/skills/eval-rubric-designer)
- [Skill Homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/eval-rubric-designer.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown with structured rubric tables, fenced judge prompts, and strict JSON output contracts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces 3-6 weighted dimensions, 1/3/5 scoring anchors, labelling guidance, and judge reliability notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
