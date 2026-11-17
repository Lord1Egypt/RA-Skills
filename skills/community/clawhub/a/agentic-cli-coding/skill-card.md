## Description:

Agentic CLI Coding provides the oce command, a validation-aware and transaction-capable toolkit for agents to read, search, modify, format, and validate source code across common languages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to make source-code changes with CLI workflows for project discovery, contextual reads, syntax validation, backups, rollback, and multi-file transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Formatter and validator workflows can execute attacker-controlled code through crafted filenames when used on untrusted checkouts.

Mitigation: Install and run only in trusted repositories; avoid format or edit/validate workflows on untrusted projects until filename interpolation issues are fixed.

Risk: Persistent PATH installation may broaden exposure in environments where the skill is not trusted.

Mitigation: Prefer direct invocation or a per-session alias unless a persistent wrapper is required.

Risk: Syntax validation does not prove an edit is logically correct.

Mitigation: Review diffs and run the target project's tests before relying on generated changes.

## Reference(s):

- [JSON Output Schema](references/json-schema.md)
- [Language Support Matrix](references/language-support.md)
- [Troubleshooting](references/troubleshooting.md)
- [Workflows](references/workflows.md)
- [ClawHub skill page](https://clawhub.ai/encryptshawn/skills/agentic-cli-coding)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The oce command can emit single-line JSON for programmatic parsing when invoked with --json.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
