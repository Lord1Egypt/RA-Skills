## Description:

Drive Axle guides users through generating drive-axle CAD drawings with the JXT/JixieTools production-sheet workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect drive-axle design parameters, submit them to the JXT/JixieTools API, review calculated values, create a guest production sheet, and monitor CAD drawing generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Drive-axle design parameters are sent to jixietools.com for calculation and drawing generation.

Mitigation: Use the skill only when users are comfortable sharing those parameters with the external service, and avoid submitting confidential specifications without authorization.

Risk: The skill includes shell command templates that can incorporate user-provided product IDs, parameter names, and values.

Mitigation: Build HTTP requests with structured JSON serialization, validate product IDs and parameter names, and avoid direct shell-string substitution.

Risk: Generated filename, guest_code, and production-sheet URLs behave like sensitive sharing links.

Mitigation: Treat these values as sensitive, share them only with intended recipients, and avoid exposing them in logs or public messages.

## Reference(s):

- [Drive Axle Skill on ClawHub](https://clawhub.ai/liv09370/skills/drive-axle)
- [JixieTools API Base](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls]

**Output Format:** [Markdown conversation with tables, JSON examples, and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language interaction flow; may produce unauthenticated production-sheet links and output file lists from the external service.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
