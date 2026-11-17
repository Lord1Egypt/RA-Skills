## Description:

Reads a Markdown file, generates a title image and section images, writes an enriched *_img.md copy with embedded PNGs, and stores generated images in a sibling img/ folder.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j3ffyang](https://clawhub.ai/user/j3ffyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and content authors use this skill to add generated header and section imagery to Markdown blog posts or documentation while preserving the original file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the skill instructs the agent to read local OpenClaw API credentials from configuration files or environment variables.

Mitigation: Use only the host-managed image generation tool with internally configured credentials; do not read, display, log, enumerate, or pass raw API secrets through the agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/j3ffyang/skills/blog-image-enricher)
- [ClawHub publisher profile](https://clawhub.ai/user/j3ffyang)

## Skill Output:

**Output Type(s):** [markdown, files, guidance]

**Output Format:** [Markdown file with embedded PNG references plus generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a sibling *_img.md file and an img/ directory while leaving the original Markdown file unchanged.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
