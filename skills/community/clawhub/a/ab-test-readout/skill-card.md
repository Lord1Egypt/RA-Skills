## Description:

Analyse a finished A/B test and write the readout: the result, whether it is statistically and practically significant, what it means, and the ship/no-ship call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, experiment owners, analysts, and growth teams use this skill to turn completed A/B test results into a concise readout with a verdict, significance assessment, guardrail review, segment notes, and a ship/no-ship recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Experiment readouts can be misleading if confidential or sensitive business metrics are shared outside an appropriate workspace.

Mitigation: Use only data that is permitted in the active workspace and redact sensitive experiment details when needed.

Risk: A/B test decisions can be distorted by missing sample-size, significance, guardrail, peeking, novelty, or segment evidence.

Mitigation: Require the readout to state assumptions, distinguish statistical from practical significance, check guardrails, and avoid declaring a winner when evidence is insufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/ab-test-readout)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/ab-test-readout.html)

## Skill Output:

**Output Type(s):** [text, markdown, analysis, guidance]

**Output Format:** [Markdown readout with a verdict, results table, risk discussion, segment cuts, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask for missing hypothesis, metric, sample size, duration, guardrail, or decision-rule inputs before completing the readout.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
