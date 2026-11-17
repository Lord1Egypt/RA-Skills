## Description:

eframe 框架快速开发技能，帮助 agents 基于 linlan-eframe 的 Spring Boot, MyBatis, Security, Vue3, and Element Plus stack create backend APIs, frontend pages, and CRUD modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linlannet](https://clawhub.ai/user/linlannet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to add business modules to the eframe framework, including database setup, model/view/api backend layers, permission annotations, and Vue frontend files. It is most useful when generating or adapting CRUD code that should follow the linlan-eframe conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable backend controller examples may be copied into business-data endpoints without explicit authorization checks on detail, export, update, delete, or similar operations.

Mitigation: Before using generated or copied controller code, add explicit permission checks for every endpoint and verify authorization tests fail closed for users without the required permissions.

## Reference(s):

- [linlan-eframe framework repository](https://gitee.com/linlannet/linlan-eframe)
- [eframe backend three-layer pattern](references/backend-layers.md)
- [eframe frontend development pattern](references/frontend-pattern.md)
- [ClawHub skill page](https://clawhub.ai/linlannet/skills/eframe-skills)

## Skill Output:

**Output Type(s):** [Code, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline Java, JavaScript, SQL, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces implementation patterns and code templates for a specific eframe application stack.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
