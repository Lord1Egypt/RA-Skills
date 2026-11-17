## Description:

Validates AI prompts for injection, role overrides, data leaks, or jailbreaks, then decides whether the agent should pass, block, or quarantine the task before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jongartmann](https://clawhub.ai/user/jongartmann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to route each user prompt through a third-party security gate before the agent begins work, stopping tasks that the service classifies as blocked or requiring human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Every user prompt is sent to a third-party gate service before work begins.

Mitigation: Use only with prompts that do not contain secrets, private source code, regulated data, or confidential business content unless the publisher provides acceptable privacy, retention, consent, and credential controls.

Risk: The remote service can block or quarantine agent work without clear local override controls.

Mitigation: Deploy only where that control model is acceptable, and route BLOCK or QUARANTINE outcomes to a documented human review path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jongartmann/skills/aegis-gate)
- [Live API](https://tower.x-loop3.com)
- [Demo](https://clawtower.x-loop3.com)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text]

**Output Format:** [Markdown instructions with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes prompts to a remote gate service and follows PASS, BLOCK, QUARANTINE, or fail-secure handling.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
