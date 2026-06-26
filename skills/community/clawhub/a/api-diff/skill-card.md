## Description: <br>
Compares OpenAPI 3.x or Swagger 2.0 specs and generates changelogs that distinguish breaking and non-breaking changes across endpoints, parameters, schemas, responses, security, server URLs, and deprecations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API platform teams use this skill to compare API versions, review OpenAPI or Swagger spec changes, generate changelogs, and gate CI builds on breaking changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The command reads local API specification files supplied by the user and includes detected differences in its output. <br>
Mitigation: Run it only on specification files intended for comparison and share generated changelogs through approved channels. <br>
Risk: The CI option can intentionally fail a build when breaking changes are detected. <br>
Mitigation: Enable fail-on-breaking only in workflows where API compatibility failures are expected and documented. <br>


## Reference(s): <br>
- [API Diff on ClawHub](https://clawhub.ai/charlie-morrison/api-diff) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands] <br>
**Output Format:** [Text, JSON, or Markdown changelog with breaking-change summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can filter to breaking changes and can exit with code 1 when breaking changes are detected.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
