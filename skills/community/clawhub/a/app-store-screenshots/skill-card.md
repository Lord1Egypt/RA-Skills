## Description:

App Store and Google Play screenshot creation with exact platform specs, covering iOS and Android dimensions, gallery ordering, device mockups, and preview videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[okaris](https://clawhub.ai/user/okaris)

### License/Terms of Use:


## Use Case:

Developers, designers, and app marketers use this skill to plan App Store and Google Play screenshot sets, choose platform-specific dimensions, order galleries, write benefit-focused captions, and generate mockup or preview-video prompts through the inference.sh CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup guidance includes running a remote shell installer, which can execute mutable remote code.

Mitigation: Prefer manual download with SHA-256 verification from the published checksums, run installation from a low-privilege environment, and avoid exposing unnecessary secrets.

Risk: Related skill installation examples use optional unpinned npx package references that may resolve differently over time.

Mitigation: Use pinned package versions where available and review resolved packages before installation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/okaris/skills/app-store-screenshots)
- [inference.sh](https://inference.sh)
- [inference.sh CLI installer](https://cli.inference.sh)
- [inference.sh CLI checksums](https://dist.inference.sh/cli/checksums.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform dimensions, screenshot ordering, caption guidance, CLI commands, and media-generation prompts.]

## Skill Version(s):

0.1.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
