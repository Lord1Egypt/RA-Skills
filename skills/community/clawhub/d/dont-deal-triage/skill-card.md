## Description:

Helps an agent provide conservative triage guidance for developers or desk workers reporting chest pain, chest pressure, left arm or jaw discomfort, shortness of breath, unusual sweating, faintness, or exhaustion-aware health concerns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaoqing404](https://clawhub.ai/user/shaoqing404)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and desk workers use this skill to get short, conservative guidance when symptoms may require emergency help or same-day medical review. It is designed to keep acute health triage action-oriented and is not a diagnosis skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat health-triage output as medical diagnosis.

Mitigation: Present the skill as conservative triage support only, and direct active emergency symptoms to emergency help or same-day medical review as appropriate.

Risk: The release package references scripts and reference files that are not included in the artifact.

Mitigation: Do not rely on the referenced local analyzer or quick-mode files unless they are supplied and reviewed in the installed package.

Risk: The skill may lead an agent to inspect limited local work-pattern data such as git timestamps while discussing health symptoms.

Mitigation: Require explicit user consent before local context inspection or local storage of health history, and keep inspection limited to the active repository signals described by the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaoqing404/skills/dont-deal-triage)
- [Server-resolved GitHub provenance](https://github.com/shaoqing404/dont-deal/tree/main/skills/dont-deal-triage)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [Concise conversational guidance or structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include urgency, reasoning_summary, recommended_action, and follow_up_questions.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
