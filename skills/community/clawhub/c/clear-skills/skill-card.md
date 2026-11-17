## Description:

This skill helps an agent clear, remove, or clean up AI agent rules, skills, and instruction files across major coding platforms on Windows, macOS, and Linux.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subingshe](https://clawhub.ai/user/subingshe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent users use this skill to identify and remove project-level or user-global rule and skill files for AI coding tools, with options for preview, backup, platform filtering, and scope filtering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete broad AI-tool configuration and workspace directories beyond narrow rule or skill files.

Mitigation: Use dry-run first, review the target list, and prefer explicit --mode and --platforms filters instead of default all-platform cleanup.

Risk: Global cleanup can affect user-level configuration across multiple AI coding tools.

Mitigation: Use project-only cleanup when possible and avoid running the script as administrator or root.

Risk: Backups may not fully protect against accidental deletion or failed recovery.

Mitigation: Keep independent backups of important configuration and avoid --no-backup unless permanent deletion is acceptable.

Risk: Non-interactive execution bypasses the manual YES confirmation.

Mitigation: Use --yes only in controlled automation after a reviewed dry-run output.

## Reference(s):

- [Platform rule file path reference](references/platforms.md)
- [ClawHub release page](https://clawhub.ai/subingshe/skills/clear-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and plain-text script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script can preview targets, back up files, and delete local AI-tool rule or configuration paths when executed.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
