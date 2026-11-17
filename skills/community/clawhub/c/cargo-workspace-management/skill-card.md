## Description:

Administers a Cargo workspace: invites teammates, creates and rotates API tokens, organizes plays, tools and agents into folders, checks roles, uploads CSVs for batch runs, and sends bug reports or feature requests to the Cargo team.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Cargo workspace administrators and developers use this skill to manage members, roles, tokens, folders, and workspace settings, and to create batch runs or send feedback through the Cargo CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make broad workspace and secret-management changes, including changes to users, roles, tokens, folders, and environment variables.

Mitigation: Confirm the active workspace and review each proposed write; pass secret values through environment variables or a secrets manager.

Risk: The documented install uses an unpinned @cargo-ai/cli@latest package.

Mitigation: Review and pin a vetted CLI version before relying on it in repeatable or automated workflows.

Risk: Diagnostic reports may include commands, errors, and resource identifiers sent to the Cargo team.

Mitigation: Review report contents and redact secrets or personal information before submission.

Risk: The security scan is partial because two referenced paths could not be resolved.

Mitigation: Review the unresolved dependencies and paths before relying on behavior the available evidence does not cover.

## Reference(s):

- [Cargo skills project homepage](https://github.com/getcargohq/cargo-skills)
- [Response shapes](artifact/references/response-shapes.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [API token examples](artifact/references/examples/tokens.md)
- [User management examples](artifact/references/examples/users.md)
- [Folder examples](artifact/references/examples/folders.md)
- [Report examples](artifact/references/examples/reports.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.7.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
