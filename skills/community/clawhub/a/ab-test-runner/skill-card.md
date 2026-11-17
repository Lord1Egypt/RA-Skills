## Description:

Design and execute A/B testing experiments for LLM prompts, agent behaviors, and content production.

This skill is ready for commercial/non-commercial use.

## Publisher:

[demo112](https://clawhub.ai/user/demo112)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt engineers, and content teams use this skill to design controlled A/B experiments for prompts, agent behaviors, engineering changes, and content variants. It helps define hypotheses, metrics, rubrics, samples, execution steps, analysis, archiving, and follow-up recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Experiment prompts, outputs, and findings may be saved under memory/experiments.

Mitigation: Avoid sensitive, confidential, or proprietary experiment data unless retention is acceptable, or ask the agent to redact details or skip archiving.

Risk: Self-scoring can inflate results or bias winner selection.

Mitigation: Use cross-scoring or an external blind evaluator when scores influence production decisions.

Risk: Small sample sizes can produce directional but not statistically reliable conclusions.

Mitigation: Use at least 10 samples per variant when possible and label smaller tests as directional signals.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/demo112/skills/ab-test-runner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON manifests, result summaries, and optional local experiment files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce experiment manifests, rubrics, scored result summaries, archived findings, and template updates.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
