## Description:

Image analysis via the MiniMax VL API for describing images, extracting text from screenshots, and analyzing photos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexburrstudio](https://clawhub.ai/user/alexburrstudio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to send local or URL-based images to MiniMax for visual description, screenshot text extraction, and photo analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends images and prompts to MiniMax for analysis.

Mitigation: Use only images and prompts you are allowed to share with MiniMax.

Risk: The skill relies on unsafe unpinned remote execution.

Mitigation: Review or pin the minimax-coding-plan-mcp dependency before use.

Risk: The skill can silently read a root-local API-key file.

Mitigation: Prefer an explicitly exported, low-scope MINIMAX_API_KEY.

Risk: The documented setup includes a curl-to-shell installer.

Mitigation: Avoid running the installer as root and review installation scripts before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexburrstudio/skills/ab-agents-vision-minimax)
- [AB Agents Vision repository](https://github.com/alexburrstudio/ab-agents-vision)
- [MiniMax platform](https://platform.minimax.io)
- [uv installer](https://astral.sh/uv/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown returned from an image-analysis command-line workflow]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MiniMax API key and sends supplied images and prompts to the MiniMax API.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
