## Description:

Workspace Guardian stops AI from scattering files by enforcing consistent naming and directory structure for generated outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lujun2508](https://clawhub.ai/user/lujun2508)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to keep AI-generated files in predictable project folders, apply consistent naming rules, and manage temporary or rejected outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes cleanup behavior for temporary, rejected, or empty files and directories.

Mitigation: Tell the agent explicitly when drafts, rejected outputs, or temporary files must be kept for audit or recovery.

Risk: Workspace organization rules can move outputs away from a user's expected location when no path is specified.

Mitigation: Specify the desired path when location matters and review the agent's saved-location confirmation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lujun2508/skills/file-rules)
- [Publisher Profile](https://clawhub.ai/user/lujun2508)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with concise file-location confirmations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create, organize, archive, or remove files according to user instructions and workspace cleanup rules.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter says 1.0.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
