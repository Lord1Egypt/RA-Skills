## Description:

A conversational self-check for suspicious investment marketing that identifies reported warning signs and points users to official license-verification resources without judging specific products or recommending investments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liujycode](https://clawhub.ai/user/liujycode)

### License/Terms of Use:

MIT-0

## Use Case:

External users can describe a stock-tip group, low-cost finance course, high-return pitch, or unfamiliar finance app in ordinary conversation. The agent gathers relevant facts, lists matched and unconfirmed indicators, and offers official verification and emergency reporting paths.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Scenario mode can present illustrative indicators as if they were user-confirmed, affecting the resulting risk report.

Mitigation: Confirm each scenario indicator with the user before treating it as a fact; leave uncertain details marked as unconfirmed.

Risk: A referenced local path was missing during partial inspection, leaving some evidence incomplete.

Mitigation: Check that the installed bundle contains the referenced material and consult it before relying on guidance that depends on it.

## Reference(s):

- [Interview guide](references/interview.md)
- [Dialogue flows and refusal guidance](references/dialog_flows.md)
- [Official verification entry points](references/check_entrances.md)
- [Case material](references/case_material.md)
- [ClawHub release page](https://clawhub.ai/liujycode/skills/fangcun-scam-radar)

## Skill Output:

**Output Type(s):** [Guidance, Markdown]

**Output Format:** [Conversational guidance and structured Markdown self-check reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports user-described indicators and unknowns with verification steps; does not decide whether a specific offering is fraudulent or recommend investments.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata, SKILL.md frontmatter, CHANGELOG.md released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
