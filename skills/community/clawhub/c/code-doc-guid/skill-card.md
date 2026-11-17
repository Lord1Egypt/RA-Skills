## Description:

Codebase navigation and documentation assistant that helps agents locate definitions, inspect dependency impact, and keep local project documentation aligned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omeletee](https://clawhub.ai/user/omeletee)

### License/Terms of Use:


## Use Case:

Developers and coding agents use this skill to index a local codebase, search symbols and concepts, inspect dependency impact before code changes, and refresh local metadata after edits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes persistent local metadata containing file paths, symbols, docstrings, and dependency relationships.

Mitigation: Review whether .trae indexing is acceptable for private or regulated repositories before installation or use.

Risk: The skill frames its dependency checks as mandatory gates for code modification workflows.

Mitigation: Treat the checks as advisory unless the project owner explicitly adopts them as required workflow policy.

## Reference(s):

- [code-doc-guid ClawHub page](https://clawhub.ai/omeletee/skills/code-doc-guid)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON or JSONL command output, Markdown dependency reports, and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local .trae metadata files, including a SQLite index and dependency graph reports.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
