## Description:

Run standardized, safety-oriented behavioral evaluations of a target AI agent using controlled diagnostic probes, anchored scoring, cited evidence, and bounded self-correction for failures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fretelli](https://clawhub.ai/user/fretelli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, evaluators, and safety reviewers use this skill to red-team or benchmark an AI agent's behavior against authority-pressure, false-premise, hallucination, and bias probes. It produces scored diagnostic reports that describe failures without redistributing harmful outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses harmful-looking adversarial prompts as controlled test stimuli.

Mitigation: Use it only for safety evaluation, relay probes to the target as stimuli, and do not execute, fulfill, or reproduce harmful payloads.

Risk: A failed target response could contain harmful or biased content.

Mitigation: Report failures with short, non-reconstructable evidence spans and summarize behavior rather than redistributing the harmful artifact.

Risk: Single model responses can be stochastic and may overstate or understate risk.

Mitigation: Run each probe at least three times in fresh contexts, report the distribution, and have consequential findings spot-checked by a human reviewer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fretelli/skills/cognitive-behavior-evaluator)
- [Publisher profile](https://clawhub.ai/user/fretelli)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic report with scored rubric entries, cited evidence, containment notes, and remediation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should contain only short, non-reconstructable evidence spans when a target fails a harmful probe.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
