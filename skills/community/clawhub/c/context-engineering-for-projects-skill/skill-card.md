## Description:

Builds team-style project context directories, module notes, agent notes, and entrypoint references for a selected codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lywhlao2025](https://clawhub.ai/user/lywhlao2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to scaffold and populate reusable project context around an existing code directory, including module navigation, agent role notes, decisions, and entrypoint references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An unsafe project name can cause the scaffold script to create persistent files outside the intended project folder.

Mitigation: Use simple project names containing only letters, digits, dots, underscores, or hyphens, and avoid untrusted project names until the script validates path containment.

Risk: The skill reads a chosen code directory and writes persistent context files.

Mitigation: Install and run it only for code directories and target roots where that read/write behavior is acceptable.

## Reference(s):

- [Content Extraction Rules](references/extraction-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated Markdown or JSONL context files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent project context files under the selected target root and does not overwrite existing files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
