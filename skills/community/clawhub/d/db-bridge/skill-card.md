## Description:

Database table bridging skill. Parses table configurations from table.json and executes SELECT / INSERT / UPDATE / DELETE operations via sql-linker. All CRUD operations are handled by sql-linker.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use db-bridge to inspect configured database table metadata and ask an agent to produce sql-linker commands for read and controlled write workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to run broad SQL read, write, update, and delete commands through an unbundled sql-linker tool without enough safeguards.

Mitigation: Install only in controlled environments where sql-linker is trusted, version-pinned, and configured with least-privileged database credentials.

Risk: Mutation commands can affect unintended rows or expose supplier contact data if free-form SQL, unsafe WHERE clauses, masking, or audit logging are not controlled.

Mitigation: Require explicit approval for INSERT, UPDATE, and DELETE, preview affected rows before mutations, avoid free-form SQL or WHERE clauses from user text, and verify masking and audit logging before using real supplier contact data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SQL command guidance for SELECT, INSERT, UPDATE, and DELETE operations through sql-linker.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
