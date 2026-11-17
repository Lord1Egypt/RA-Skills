## Description:

Ensures file operations like delete, move, rename, overwrite, publish, upload, export, or bulk edit are scoped, reversible, authorized, and limited to intended user files only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make file-sensitive workflows pause for scope, authorization, reversibility, and data-handling checks before deleting, moving, overwriting, publishing, uploading, exporting, or bulk-editing user files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risky file operations may delete, overwrite, move, publish, upload, or bulk-edit files outside the user's intended scope.

Mitigation: Confirm the exact target paths or bounded folder, prefer dry-runs, diffs, backups, or copy-before-move workflows, and require explicit approval for destructive, recursive, cross-folder, publish, upload, or broad operations.

Risk: Review payloads for file operations may expose raw file contents, secrets, private records, full directory dumps, or unrelated user files.

Mitigation: Use redacted path summaries when sufficient, avoid raw contents and sensitive values, and keep review payloads limited to task, operation, target scope, risk, authorization, reversibility, scope, and recommendation fields.

Risk: An unavailable or untrusted checker could give users a false sense of safety before a file operation.

Mitigation: Use only approved host tools or configured API connectors for checker workflows, or fall back to manual review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mindbomber/skills/aana-file-operation-guardrail)
- [README](artifact/README.md)
- [Skill Instructions](artifact/SKILL.md)
- [File Operation Review Schema](artifact/schemas/file-operation-review.schema.json)
- [Redacted File Operation Review Example](artifact/examples/redacted-file-operation-review.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown guidance with an optional redacted JSON review payload pattern]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not install dependencies, execute commands, write files, call services, or persist memory by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
