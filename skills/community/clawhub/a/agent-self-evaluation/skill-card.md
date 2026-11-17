## Description:

Self-evaluate task completion across 5 axes: accuracy, completeness, clarity, actionability, and conciseness, using evidence for low scores.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill after substantial or multi-step work to produce a structured self-evaluation report, identify concrete gaps, and decide whether immediate fixes are needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad triggering can add extra review text after routine tasks.

Mitigation: Use the skill mainly for substantial work, multi-step workflows, debugging sessions, design analysis, or explicit self-evaluation requests.

Risk: Self-evaluation may overstate quality if the agent does not cite concrete evidence for low scores.

Mitigation: Require each score below 5 to cite the specific missing, incorrect, unclear, or non-actionable element.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/agent-self-evaluation)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown self-evaluation report or concise checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes five-axis scores, evidence for non-perfect scores, an average score, prioritized improvements, and a self-check.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
