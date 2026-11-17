## Description:

Generates clutch CAD drawings by guiding users through product selection, parameter collection, calculation, and guest production-sheet creation through jixietools.com.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liv09370](https://clawhub.ai/user/liv09370)

### License/Terms of Use:

MIT-0

## Use Case:

External users and engineers use this skill to configure clutch design parameters, review calculated values, and request CAD drawing generation through the JXT mechanical parts service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends clutch design parameters to jixietools.com and receives a guest access link.

Mitigation: Use only when the user is comfortable sharing those design parameters with the third-party service.

Risk: The artifact shows shell-command patterns that could become unsafe if raw user input or returned filenames are interpolated into commands.

Mitigation: Implement API calls with a structured HTTP client or JSON serializer and avoid passing untrusted values through shell interpolation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liv09370/skills/clutch)
- [JixieTools API Base](https://jixietools.com/api/v1)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, API calls]

**Output Format:** [Markdown conversation with tables, JSON summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a guest access link and lists generated output files when the external service completes.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
