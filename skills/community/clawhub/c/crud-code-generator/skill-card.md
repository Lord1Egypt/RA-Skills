## Description: <br>
Generates CRUD code for database table objects across Java/Spring Boot backends and Vue 2 frontends from DDL SQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[endcy](https://clawhub.ai/user/endcy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to scaffold management CRUD implementations from database DDL, including backend Java layers, SQL files, optional Vue 2 frontend pages, and validation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can write many Java, Vue, and SQL files into a project. <br>
Mitigation: Use it in a version-controlled workspace, confirm backend and frontend roots before generation, and review generated diffs before applying or committing them. <br>
Risk: Generated SQL and CRUD logic may not match project-specific authorization, data, or schema requirements. <br>
Mitigation: Review generated SQL, permissions, entity mappings, query fields, and controller behavior before deploying the changes. <br>
Risk: Local build validation can run Maven or npm commands in the target repository. <br>
Mitigation: Avoid running Maven or npm validation in untrusted repositories, and inspect project scripts before executing them. <br>


## Reference(s): <br>
- [CRUD Code Generator on ClawHub](https://clawhub.ai/endcy/crud-code-generator) <br>
- [Java Templates](references/java-templates.md) <br>
- [SQL Templates](references/sql-templates.md) <br>
- [Vue Templates](references/vue-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated code, SQL snippets, shell commands, and file lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write multiple project files and may run local Maven or npm validation when requested.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and README version table) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
