## Description:

Api Design Doc helps developers generate standardized API design documentation from requirements or database DDL, including endpoint definitions, request and response examples, error codes, naming conventions, and page-to-API mappings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnsunxuefeng](https://clawhub.ai/user/cnsunxuefeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn product requirements, business scenarios, or database DDL into a standardized API design document for implementation and front-end/back-end integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes to a fixed Markdown path, which may overwrite an existing API design document.

Mitigation: Confirm the target path and review any existing doc/API接口设计文档.md before allowing the agent to write the file.

Risk: Generated API specifications may be incomplete or inconsistent with the actual requirements, database schema, or service behavior.

Mitigation: Review generated endpoints, parameters, response examples, and error codes against the source requirements and DDL before implementation.

## Reference(s):

- [Error Codes Reference](references/error-codes.md)
- [API Specification Template](references/api-spec-template.md)
- [Naming Conventions](references/naming-conventions.md)
- [API Design Best Practices](references/best-practices.md)
- [API Response Template](assets/templates/api-response-template.json)
- [ClawHub Skill Page](https://clawhub.ai/cnsunxuefeng/skills/api-design-doc)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Configuration]

**Output Format:** [Markdown document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates doc/ if needed and uses the fixed output filename doc/API接口设计文档.md.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
