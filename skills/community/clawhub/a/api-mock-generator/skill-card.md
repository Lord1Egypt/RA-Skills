## Description:

Generate mock API servers and static JSON fixtures from OpenAPI 3.x and Swagger 2.0 specs for frontend development, testing, demos, or CI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create local mock API servers, static JSON fixtures, route listings, and sample responses from OpenAPI or Swagger specifications for frontend development, testing, demos, or CI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local API specification files and can generate mock JSON files into a user-selected directory.

Mitigation: Use trusted API specs and choose an output directory that does not contain important existing files.

Risk: The live mock server can be bound to a host and port selected by the user.

Mitigation: Keep the default localhost binding unless intentional network access is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/api-mock-generator)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands and JSON file or server output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local HTTP responses, route listings, sample JSON responses, static mock JSON files, and a manifest.json file.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
