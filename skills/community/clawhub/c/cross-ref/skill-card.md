## Description:

Audit a named GitHub repository for duplicate pull requests and missing issue-to-PR links, producing a read-only report first with optional approval-gated comment posting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucksberg](https://clawhub.ai/user/glucksberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to scan a specified GitHub repository for duplicate pull requests and missing issue-to-PR links. It helps them review evidence-backed clusters and decide whether to keep the run read-only or post approved cross-reference comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository-controlled text and local workspace state can affect analysis prompts or command behavior.

Mitigation: Use the skill only on repositories that are acceptable to process in the configured agent runtime, validate inputs, and inspect generated reports before acting.

Risk: Approved comment posting can publish incorrect or misleading GitHub comments if findings are accepted too quickly.

Mitigation: Keep the default plan or dry-run mode until each exact comment body is reviewed, require approved-comments.json plus --execute, and use read-only credentials for analysis.

## Reference(s):

- [cross-ref on ClawHub](https://clawhub.ai/glucksberg/skills/cross-ref)
- [Cross-Ref Principles](artifact/references/principles.md)
- [Comment Approval and GitHub API Safety](artifact/references/commenting-strategy.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON result files, and shell command invocations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report-first workflow; optional comment posting requires a reviewed approval file and an explicit execution flag.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
