## Description:

Cross Check helps an agent surface assumptions, blind spots, and confidence notes, and can run lite, deep, or optional two-model verification when the user opts in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tommot2](https://clawhub.ai/user/tommot2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use Cross Check to challenge important responses, compare reasoning paths, and identify assumptions before acting on an answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cross Check suggestions or confidence notes can interfere with workflows that require strict response formatting.

Mitigation: Turn suggestions off with 'cross-check off' or leave HEARTBEAT auto-suggestions disabled when exact output shape matters.

Risk: Optional two-model verification shares the problem context and extracted assumptions with a configured verifier model and uses additional tokens.

Mitigation: Use two-model mode only when the configured verifier is acceptable for the task and the user explicitly requests it.

Risk: Verification summaries may still miss important facts or overstate confidence.

Mitigation: Treat Cross Check output as advisory and review conclusions before making high-impact decisions.

## Reference(s):

- [Cross Check ClawHub skill page](https://clawhub.ai/tommot2/skills/cross-check)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text confidence notes and compact verification summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Compact by default; lite output is capped at 8 lines and deep output at 15 lines.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
