## Description:

Generate personalized 120-day career success plans based on professional assessment data and onboarding goals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, HR teams, managers, career coaches, and professionals use this skill to generate personalized 120-day onboarding and career transition plans from role, experience, and goal data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Employee onboarding and career assessment details are sent to a disclosed external API.

Mitigation: Confirm organizational approval, consent, and data-handling policy fit before use.

Risk: Assessment payloads may include direct identifiers, manager names, confidential performance information, or sensitive HR records.

Mitigation: Send only necessary information and avoid sensitive or identifying details unless policy approval is in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/career-success-planner)
- [OpenAPI specification](artifact/openapi.json)
- [API documentation](https://api.mkkpro.com:8073/docs)
- [Career planner API route](https://api.mkkpro.com/career/120-day-planner)

## Skill Output:

**Output Type(s):** [guidance, text, json]

**Output Format:** [JSON career plan with structured phases, weekly focus, skill development path, risk mitigation, and checkpoints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sessionId, timestamp, and assessmentData; userId is optional.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
