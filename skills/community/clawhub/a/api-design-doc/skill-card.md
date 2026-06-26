## Description: <br>
Generates a standardized API design document from requirements or database DDL, including endpoint definitions, request and response examples, error codes, naming guidance, and RESTful design conventions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnsunxuefeng](https://clawhub.ai/user/cnsunxuefeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to turn product requirements or database DDL into a REST-style API design document for implementation and frontend-backend coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes to a fixed project path, doc/API接口设计文档.md, which may replace an existing API design document if the agent proceeds without checking. <br>
Mitigation: Check whether the file already exists, confirm that writing to the fixed path is acceptable, and review the generated Markdown before relying on it. <br>


## Reference(s): <br>
- [API specification template](references/api-spec-template.md) <br>
- [API design best practices](references/best-practices.md) <br>
- [Error code specification](references/error-codes.md) <br>
- [Naming conventions](references/naming-conventions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Guidance] <br>
**Output Format:** [Markdown document written to doc/API接口设计文档.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates doc/ if needed and writes one API design document.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
