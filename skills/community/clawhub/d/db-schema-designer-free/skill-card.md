## Description: <br>
Helps developers and small teams design flexible SQLite soft-schema databases with raw, soft-field, and business-view layers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and small teams use this skill to plan SQLite schemas for early-stage projects where fields and query needs may change. It can guide schema design, generate SQL examples, and propose local database setup and query commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide local SQLite writes or command execution that changes a project database. <br>
Mitigation: Confirm the target project path, database file, and SQL statements before allowing write or exec actions. <br>
Risk: A callback URL could send processing results to an unintended destination. <br>
Mitigation: Use callback_url only when the destination is explicitly trusted and the transmitted data is understood. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include SQLite schema definitions, validation checklists, and local command examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
