## Description: <br>
Generate on-aesthetic images for brands by combining a persistent brand aesthetic with per-image editorial art direction and passing the composed prompt to a Gemini-backed image generator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[machinesofdesire](https://clawhub.ai/user/machinesofdesire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, brand teams, publishers, and agents use this skill to install a reusable visual aesthetic, compose art-directed image briefs, generate single images or batches, and iterate until images match a publication or brand voice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Image briefs and brand aesthetic text are sent to the underlying Gemini-backed generator. <br>
Mitigation: Do not include secrets, regulated data, confidential launch details, or other sensitive material in briefs or aesthetic.md. <br>
Risk: The skill requires a sensitive credential through GEMINI_API_KEY for image generation. <br>
Mitigation: Provide the key through the environment only, keep it out of prompts and saved configuration, and rotate it if it is exposed. <br>
Risk: NANO_BANANA_SCRIPT can redirect execution to a local generator script. <br>
Mitigation: Set NANO_BANANA_SCRIPT only to a trusted local nano-banana-pro generate_image.py path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/machinesofdesire/art-director) <br>
- [Publisher profile](https://clawhub.ai/user/machinesofdesire) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Preset guide](artifact/presets/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance, CLI commands, composed prompts, status text, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, GEMINI_API_KEY, and a trusted local nano-banana-pro generator path when overridden.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
