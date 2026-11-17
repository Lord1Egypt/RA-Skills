## Description:

Generates infographic image card series with 12 visual styles, 8 layouts, and 3 color palettes for social media engagement.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimliu](https://clawhub.ai/user/jimliu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and agent users use this skill to turn long-form or complex content into a 1-10 card infographic series for Xiaohongshu, WeChat, and similar social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The codex-imagegen fallback can run local or downloaded code before rendering images.

Mitigation: Prefer native image generation or a trusted installed backend; use the codex-imagegen fallback only after reviewing the selected executable path.

Risk: BAOYU_CODEX_IMAGEGEN_BIN can redirect execution to an arbitrary local target.

Mitigation: Set BAOYU_CODEX_IMAGEGEN_BIN only to a reviewed and trusted file.

Risk: The fallback may install and run Bun through npx.

Mitigation: Require separate approval before allowing npx -y bun runtime installation.

Risk: Prompt guidance for sensitive or copyrighted figures may conflict with platform safety requirements.

Mitigation: Apply platform safety policy before following figure-related prompt guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jimliu/skills/baoyu-xhs-images)
- [OpenClaw Homepage](https://github.com/JimLiu/baoyu-skills#baoyu-xhs-images)
- [Style Presets](artifact/references/style-presets.md)
- [Prompt Assembly Guide](artifact/references/workflows/prompt-assembly.md)
- [Xiaohongshu Outline Template](artifact/references/workflows/outline-template.md)
- [Codex Imagegen Wrapper Invocation](artifact/references/codex-imagegen.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration, Shell commands]

**Output Format:** [Markdown instructions, prompt files, outline files, and backend-specific image generation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reproducibility prompt files before image generation and expects raster image outputs from an available backend.]

## Skill Version(s):

2.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
