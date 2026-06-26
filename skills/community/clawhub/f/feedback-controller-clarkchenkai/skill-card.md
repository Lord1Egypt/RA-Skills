## Description: <br>
Feedback Controller helps agents diagnose execution drift and choose a correction path using a closed-loop protocol and fixed Markdown output contract. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarkchenkai](https://clawhub.ai/user/clarkchenkai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, automation builders, and agent operators use this skill to compare a target state with current output, localize drift, and decide whether to retry, adjust scope, switch tools, or escalate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may activate broadly and influence correction decisions in multi-step work. <br>
Mitigation: Review the proposed diagnosis and correction strategy before relying on it, and disable implicit invocation or call the skill explicitly for approval-sensitive tasks. <br>
Risk: Repeated correction loops can hide missing authority, policy conflicts, or unavailable evidence. <br>
Mitigation: Use the skill's escalation decision and stop condition to hand off when approval, policy, or missing context blocks safe correction. <br>


## Reference(s): <br>
- [Correction Patterns](references/correction-patterns.md) <br>
- [Escalation Rules](references/escalation.md) <br>
- [Wiener Reference](references/wiener.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with a six-part diagnostic structure] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Ends with Target State, Current State, Observed Deviation, Error Source, Correction Strategy, and Escalation Decision sections.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
