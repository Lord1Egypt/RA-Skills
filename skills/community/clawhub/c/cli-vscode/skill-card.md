## Description:

Command-line interface for VSCode to open files, install and list extensions, manage workspaces, and check editor status with JSON output support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaising-openclaw1](https://clawhub.ai/user/kaising-openclaw1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agent builders use this skill to automate common VSCode actions from a command line or JSON-oriented workflow, including opening files, managing extensions, adding workspace folders, and checking editor status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent install arbitrary VSCode extensions.

Mitigation: Require explicit approval for install-extension commands and verify extension IDs and publishers before installation.

Risk: The skill can add folders to a VSCode workspace, which may expose sensitive files to editor tooling or extensions.

Mitigation: Add only necessary folders and avoid sensitive directories unless the user has approved the workspace change.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kaising-openclaw1/skills/cli-vscode)
- [Skill Documentation](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Command-line text or JSON responses, with Markdown documentation and bash examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VSCode and the code command-line tool; can install VSCode extensions and add folders to the active workspace.]

## Skill Version(s):

1.0.0 (source: server release and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
