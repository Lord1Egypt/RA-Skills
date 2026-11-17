## Description:

Dedicated File Manager helps agents manage, organize, classify, rename, archive, and clean files and folders using workspace setup, automated sorting, manifests, reports, and conflict handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qshan1](https://clawhub.ai/user/qshan1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent structured rules and helper scripts for organizing workspaces, classifying files, maintaining manifests, producing reports, and safely moving or renaming files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move, rename, archive, and scan user files, which may disrupt a workspace if applied to the wrong directory.

Mitigation: Use dry-run mode first, point the skill only at a narrow workspace, review the proposed plan, and back up important folders before allowing non-dry-run organization.

Risk: Weekly automation can repeatedly reorganize inbox or temporary files with limited ongoing review.

Mitigation: Disable weekly automation unless needed, or review the automation configuration and generated reports before relying on scheduled organization.

Risk: Rename and move operations can affect project references or user expectations even when files are not deleted.

Mitigation: Require confirmation before moves and renames, especially for code projects, broad roots, and batch operations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/qshan1/skills/dedicated-file-manager)
- [File Types Reference](references/file-types.md)
- [Naming Rules Reference](references/naming-rules.md)
- [Project Templates Reference](references/project-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown guidance with inline shell commands, JSON reports, configuration snippets, manifests, and file-organization reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or execute file moves, renames, archive actions, directory creation, manifest updates, and dry-run reports depending on user confirmation and tool access.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
