## Description:

Analyzes a project and generates Harness Engineering documentation for common backend and frontend stacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangjiayu139](https://clawhub.ai/user/zhangjiayu139)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to bootstrap repository documentation, architecture notes, quality grading, CI configuration, and optional architecture tests for projects using frameworks such as Spring Boot, React, Vue, NestJS, Express, Django, FastAPI, and Go Gin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can overwrite repository policy, documentation, CI workflow, and Java architecture test files.

Mitigation: Run it in a clean branch and review the diff before committing generated changes.

Risk: Generated documentation and architecture layers may not match the project's actual structure.

Mitigation: Review and edit generated docs, CI commands, and architecture tests before relying on them.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, YAML workflow configuration, and optional Java test code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or overwrite repository documentation, CI workflow, and architecture test files in the current project.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
