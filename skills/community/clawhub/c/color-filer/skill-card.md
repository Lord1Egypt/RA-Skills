## Description:

Color-Filer helps agents analyze and organize local folders with emoji-based file and folder labels, zero-padded ordering, batch renaming, workspace organization, and naming guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyrilcao](https://clawhub.ai/user/cyrilcao)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect local workspaces, preview naming changes, and organize personal knowledge bases, project folders, and archived resources with consistent visual naming conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can recursively rename, move, copy, and create files or folders in a target workspace.

Mitigation: Use dry-run first, run on a small backed-up workspace, review the previewed changes, and avoid automatic confirmation for unfamiliar operations.

Risk: Configuration loaded through the --config option is executed as Python code.

Mitigation: Use --config only with files you personally inspected and trust; do not run configuration files from unknown sources.

## Reference(s):

- [Color-Filer ClawHub Skill Page](https://clawhub.ai/cyrilcao/skills/color-filer)
- [Color-Filer API Reference](references/api_reference.md)
- [Color-Filer Naming Rules](references/naming_rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, script usage examples, naming rules, and local file-operation outputs when scripts are run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May preview or perform recursive rename, move, copy, backup, and directory creation operations depending on user-selected script flags.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
