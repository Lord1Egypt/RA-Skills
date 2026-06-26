## Description: <br>
API code generator. Generate RESTful endpoints, GraphQL schemas, OpenAPI/Swagger docs, API clients, mock servers, authentication, rate limiting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold API endpoints, schemas, clients, mock servers, auth snippets, rate limiting examples, tests, and API documentation templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated API, authentication, and rate limiting code may be incomplete or unsuitable for a production service as emitted. <br>
Mitigation: Review, adapt, scan, and test generated code before integrating it into an application. <br>
Risk: The REST scaffolding script can create a local api-generator data directory and append command history under the user's data directory unless APIGEN_DIR is set. <br>
Mitigation: Set APIGEN_DIR to an appropriate workspace-specific location or review the local history file handling before use. <br>


## Reference(s): <br>
- [BytesAgain homepage](https://bytesagain.com) <br>
- [ClawHub skill page](https://clawhub.ai/ckchzh/api-generator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Terminal text and generated code snippets printed to stdout.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated scaffolds should be reviewed, edited, and tested before production use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
