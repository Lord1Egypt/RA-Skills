## Description:

Analyzes finished A/B tests by computing lift, p-value, and confidence intervals, checking guardrails and validity, and producing a clear ship, no-ship, iterate, or re-run recommendation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Product managers, analysts, and engineers use this skill to turn finished A/B test data into an honest statistical readout with guardrail checks, validity notes, and a decision recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence product launch decisions from A/B test results.

Mitigation: Review statistical assumptions and independently verify calculations before using the recommendation for high-stakes launches.

Risk: The referenced significance helper script is not included in the package.

Mitigation: Use a trusted calculator or provide and review the helper before relying on command examples.

Risk: Invalid experiment setup, peeking, sample-ratio mismatch, novelty effects, or guardrail degradation can make a readout misleading.

Mitigation: Require planned sample and duration details, guardrail metrics, and validity checks before acting on the result.

## Reference(s):

- [Experiment Readout on ClawHub](https://clawhub.ai/mohitagw15856/skills/experiment-readout)
- [Experiment Readout homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/experiment-readout.html)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown readout with tables, statistics, validity checks, and optional bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires experiment data, hypothesis, guardrail metrics, and test setup details; verify calculations independently for high-stakes launches.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
