## Description:

Validate .env files against schemas, compare environments, detect common mistakes, auto-generate schemas, and type-check values with text, JSON, and markdown output plus CI-friendly exit codes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate environment configuration files, compare environments before deployment, generate schema files, and produce CI-friendly validation reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated schemas, JSON reports, CI logs, or diff artifacts can expose secrets from .env files.

Mitigation: Use sanitized .env.example files for schema generation, inspect generated outputs before sharing or committing them, and keep reports out of public logs unless secrets have been removed.

Risk: The skill reads local environment files that may contain sensitive configuration values.

Mitigation: Run it only on env files you are authorized to inspect and handle all output as sensitive until reviewed.

## Reference(s):

- [Schema Format Reference](references/schema-format.md)
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/env-config-validator)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration]

**Output Format:** [Text, JSON, or Markdown reports with optional generated JSON schema files and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses CI-oriented exit codes: 0 for no issues, 1 for warnings or diffs, and 2 for errors.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
