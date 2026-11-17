## Description:

Detects potential infinite loops and runaway token usage risks in Claw AI workflows by analyzing retry, recursion, and termination conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showmethemoney2023](https://clawhub.ai/user/showmethemoney2023)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to review Claw workflows, task descriptions, or prompts for retry, recursion, termination, and token-amplification risks before deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may submit sensitive workflows or prompts for analysis.

Mitigation: Avoid pasting secrets or highly sensitive internal workflows unless that is approved for the operating environment.

Risk: Checklist-style analysis may miss or overstate runaway loop and token-cost risks.

Mitigation: Use the findings as review guidance alongside concrete runtime controls such as retry limits, token limits, recursion limits, and behavior monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/showmethemoney2023/skills/claw-runaway-loop-detector)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown risk analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a risk level, detected loop triggers, token amplification estimate, token impact range, and recommended safeguards.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
