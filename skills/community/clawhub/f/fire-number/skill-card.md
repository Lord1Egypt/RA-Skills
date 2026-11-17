## Description:

Computes a financial-independence (FIRE) target, years to target, sensitivity grid, and ignored-risks list with assumptions labeled.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to model a FIRE target from current invested savings, monthly contributions, target annual spend, and explicit return and withdrawal-rate assumptions. It is intended to produce an educational range with labeled assumptions rather than a precise retirement date or financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat FIRE projections as precise financial advice or a guaranteed retirement timeline.

Mitigation: Present results as educational modeling, label every assumption, provide a sensitivity range, avoid exact retirement dates, and direct users to a licensed professional before acting.

Risk: The model can omit material planning factors such as taxes, sequence-of-returns risk, and spending drift.

Mitigation: State the ignored risks in the output and keep the result framed as a simplified scenario analysis.

Risk: Users may provide unnecessary personal financial details while requesting a calculation.

Mitigation: Ask only for the minimum inputs needed for the model and avoid collecting unrelated personal information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/fire-number)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/fire-number.html)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis with optional shell command examples and optional JSON helper output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes labeled assumptions, a return-by-withdrawal-rate sensitivity grid, ignored-risks list, and educational disclaimer.]

## Skill Version(s):

50.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
