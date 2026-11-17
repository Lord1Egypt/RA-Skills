## Description:

Analyzes CSAT, NPS, and CES survey data to compute scores, theme verbatims, surface trends and benchmarks, and produce prioritized actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mohitagw15856](https://clawhub.ai/user/mohitagw15856)

### License/Terms of Use:

MIT-0

## Use Case:

Customer experience, product, support, and operations teams use this skill to turn CSAT, NPS, or CES survey responses into a structured readout with score distribution, trend context, verbatim themes, segment differences, and prioritized actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Survey verbatims may contain customer or employee personal data.

Mitigation: Provide only survey data that is appropriate to share with the agent, and remove or mask personal data before analysis when possible.

Risk: The skill references a calculator script that is not present in the inspected package.

Mitigation: Verify NPS, CSAT, and CES calculations manually or with a trusted helper, and state the formula used in the readout.

Risk: Small samples, missing segment context, or absent benchmarks can make trends and recommendations misleading.

Mitigation: Flag low response counts and missing context, separate assumptions from findings, and avoid overclaiming trend or benchmark conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mohitagw15856/skills/csat-nps-analysis)
- [Skill homepage](https://mohitagw15856.github.io/pm-claude-skills/skill/csat-nps-analysis.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown readout with score calculations, themed analysis, segment notes, and prioritized action recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include representative survey quotes supplied by the user and should state assumptions, formulas, low sample-size concerns, and missing benchmark context.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
