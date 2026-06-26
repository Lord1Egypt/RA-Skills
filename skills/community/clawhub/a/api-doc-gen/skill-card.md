## Description: <br>
Generates API documentation from Flask, Django DRF, FastAPI, Express.js, NestJS, and generic code into Markdown, OpenAPI 3.0, or Postman Collection formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shenghoo123-png](https://clawhub.ai/user/shenghoo123-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to inspect API source code, infer routes and parameters, and generate consistent API documentation for implementation, review, and debugging workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated documentation may reveal internal API names, routes, parameters, or response shapes from the project being analyzed. <br>
Mitigation: Run the skill only on project directories intended for documentation and review generated files before sharing them externally. <br>
Risk: Dependency hygiene issues were noted for pytest and PyYAML. <br>
Mitigation: Install the skill in an isolated environment and pin or lock pytest and PyYAML to reviewed versions before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shenghoo123-png/api-doc-gen) <br>
- [Publisher Profile](https://clawhub.ai/user/shenghoo123-png) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown, OpenAPI 3.0 JSON, OpenAPI 3.0 YAML, or Postman Collection JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write generated documentation files or print generated output to standard output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
