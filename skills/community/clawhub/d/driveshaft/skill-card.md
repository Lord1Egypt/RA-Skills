## Description:

Generates CAD drawing workflows for universal driveshaft products by guiding users through product selection, parameter collection, calculation review, and guest production-sheet creation on jixietools.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect driveshaft design parameters, call the JXT mechanical parts API, review calculated values, and create no-login guest production sheets for CAD drawing generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-supplied values could be unsafe if inserted literally into shell command templates.

Mitigation: Use structured JSON serialization or a shell-free HTTP client before submitting user-entered values.

Risk: No-login guest links may expose generated design outputs to anyone who receives the link.

Mitigation: Share guest links only with intended recipients and avoid submitting sensitive design parameters unless this exposure is acceptable.

## Reference(s):

- [ClawHub Driveshaft skill page](https://clawhub.ai/liv09370/skills/driveshaft)
- [Jixietools API base URL](https://jixietools.com/api/v1)
- [Jixietools driveshaft product listing endpoint](https://jixietools.com/api/v1/products?category_id=8)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown guidance with inline curl commands, JSON examples, and review tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Chinese user-facing dialogue and stepwise confirmation before continuing the CAD drawing workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
