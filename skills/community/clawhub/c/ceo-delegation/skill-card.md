## Description:

CEO Delegation is a Chinese-language workflow that guides an agent to delegate tasks to sub-agents, monitor progress, arrange independent review, and report completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eisonme](https://clawhub.ai/user/eisonme)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent users use this skill to coordinate multi-step work through delegated execution, progress monitoring, independent acceptance review, and final reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task content may be sent to additional sub-agents during delegated execution.

Mitigation: Avoid using the skill for credentials, private code, personal data, or sensitive business tasks unless explicit consent, scoping, and redaction controls are in place.

Risk: The workflow encourages inspecting recent session messages for monitoring.

Mitigation: Limit monitoring to scoped task sessions and avoid exposing unrelated or sensitive session history.

Risk: The workflow encourages writing outcomes to memory without clear opt-in controls.

Mitigation: Review and approve any persistent memory writes, and redact confidential or personal information before storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eisonme/skills/ceo-delegation)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, Shell commands]

**Output Format:** [Markdown guidance with tool-call examples and progress-report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are primarily delegation instructions, review checklists, status reports, and monitoring command guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
