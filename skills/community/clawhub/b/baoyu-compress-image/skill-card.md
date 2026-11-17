## Description:

Compresses images to WebP (default) or PNG with automatic tool selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to reduce image file size, convert images to WebP, PNG, or JPEG, and process individual files or image directories from an agent-guided command line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The compression workflow can change or overwrite image files by default.

Mitigation: Use copied or backed-up images, prefer the --keep option, and check outputs before running recursive mode on important directories.

Risk: If Bun is unavailable, the documented fallback may fetch an unpinned runtime package through npx.

Mitigation: Install Bun through a trusted pinned process before using the skill instead of relying on npx -y bun.

Risk: Project EXTEND.md files can alter default compression behavior.

Mitigation: Treat EXTEND.md files as untrusted unless you control them, and review their settings before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimliu/skills/baoyu-compress-image)
- [Publisher Profile](https://clawhub.ai/user/jimliu)
- [Project Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-compress-image)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce compressed image files and size-reduction summaries when the generated command is run.]

## Skill Version(s):

1.117.2 (source: server release metadata; artifact frontmatter lists 1.56.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
