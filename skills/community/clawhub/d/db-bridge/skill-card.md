## Description: <br>
Database table bridging skill. Parses table configurations from table.json and executes SELECT / INSERT / UPDATE / DELETE operations via sql-linker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to inspect configured database tables and route SELECT, INSERT, UPDATE, and DELETE requests through sql-linker using table metadata from table.json. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward direct database writes and deletes through sql-linker. <br>
Mitigation: Use read-only mode by default where possible, require explicit approval before UPDATE or DELETE, and preview affected rows before making changes. <br>
Risk: Raw WHERE clauses or broad operations can affect unintended rows. <br>
Mitigation: Prefer parameterized APIs over raw CLI WHERE clauses and verify the target records with SELECT queries before mutation. <br>
Risk: Audit records lose value if user identity or session context is inaccurate. <br>
Mitigation: Require accurate user labels and session identifiers for write operations and preserve audit context when invoking sql-linker. <br>


## Reference(s): <br>
- [db-bridge ClawHub release](https://clawhub.ai/cloudcode-hans/db-bridge) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Database effects depend on sql-linker permissions, read-only settings, and the configured table metadata.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
