## Description: <br>
Provides a 3Q quality-control workflow for pre-checks, rapid review, deep scoring, blind review, and decision checks across writing, code, documents, and complex agent outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qh582](https://clawhub.ai/user/qh582) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, analysts, and agent users use this skill to add structured quality gates before delivery, after subtasks, and before major decisions. It helps an agent surface missing context, contradictions, weak assumptions, scoring gaps, and cases that need deeper or blind review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as quality check, pre-check, blind review, and related Chinese terms can activate the workflow unintentionally. <br>
Mitigation: Use explicit 3Q phrasing when the workflow is desired, and adjust or avoid broad triggers in environments where predictable activation matters. <br>
Risk: Deep 3Q checks and blind review can add time and token cost to routine tasks. <br>
Mitigation: Use rapid 3Q for routine subtasks and reserve deep scoring or blind review for complex work, high-impact decisions, or repeated quality failures. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qh582/3q-quality-system) <br>
- [Three-Dimensional Expansion](references/three-dimensions.md) <br>
- [3Q Daily Check Template](references/daily-check-template.md) <br>
- [Decision Checklist](references/decision-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown guidance, checklists, scoring tables, and short review summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable code output is required; deep checks and blind review can increase response time and token use.] <br>

## Skill Version(s): <br>
7.11.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
