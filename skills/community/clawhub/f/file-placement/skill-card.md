## Description:

Enforces file placement rules for documentation and scripts, including required locations for Markdown files, shell scripts, and organized project documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[urbantech](https://clawhub.ai/user/urbantech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to keep documentation and script outputs in expected project directories instead of creating clutter in root or backend folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has a broad activation scope and project-specific placement rules, so it may influence file placement in repositories where these paths are not intended.

Mitigation: Install it only for the target project or narrow its activation when global Markdown and shell-script placement guidance is not wanted.

Risk: The artifact includes hard-coded absolute project paths, which can route documentation or scripts incorrectly if the workspace layout differs.

Mitigation: Confirm the repository path assumptions before using the skill, and update the placement mapping if the project moves or changes structure.

## Reference(s):

- [Directory Mapping - Complete Reference](references/directory-mapping.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with file path patterns and placement rules]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code; behavior is limited to agent guidance for placing documentation and script files.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
