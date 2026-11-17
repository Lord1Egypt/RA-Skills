## Description:

Use when users ask to generate Java code from database tables with EasyCode-style templates, including parsing db config, remembering last-used generation settings, resolving output paths from base package, and producing a file generation plan/execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huhua1990](https://clawhub.ai/user/huhua1990)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn database table selections and EasyCode template settings into Java file generation plans and rendered project files. It supports MyBatisPlus and custom template groups, path resolution from a base package, optional JDBC metadata lookup, and reuse of prior generation settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles database connection details and local generation state.

Mitigation: Avoid entering real database passwords unless state persistence is reviewed and fixed; prefer table_columns where possible and do not store plaintext passwords.

Risk: JDBC metadata lookup and rendering can use local JDBC driver jars.

Mitigation: Only provide trusted JDBC driver jars and review driver paths before use.

Risk: Execution can write project files and optional project formatting can run local commands.

Mitigation: Review the pre-write file list and overwrite candidates before execute; enable project formatting only after the exact command is reviewed and trusted.

Risk: The security verdict is suspicious because the skill handles secrets and local command execution.

Mitigation: Review the skill carefully before installing and remove hardcoded database defaults before using it with sensitive systems.

## Reference(s):

- [Function schema](references/function-schema.json)
- [Template groups](references/template-groups.md)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON specifications, shell commands, and generated Java project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation can preview a file plan before writing files; execution may write Java source files and optionally run project formatting.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
