## Description:

Generates brand-consistent editorial images by combining a persistent aesthetic file with per-image art direction and using nano-banana-pro (Gemini) for image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[machinesofdesire](https://clawhub.ai/user/machinesofdesire)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, brand teams, and agents use this skill to turn a brand aesthetic and a specific editorial brief into image-generation prompts and saved image outputs for publications, essays, newsletters, reports, and longform product marketing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image briefs and the aesthetic file are sent through a Gemini-backed image-generation workflow.

Mitigation: Do not include confidential, regulated, or sensitive content unless that use is approved for the operator's workflow.

Risk: The NANO_BANANA_SCRIPT override can point execution at a local generator script.

Mitigation: Set NANO_BANANA_SCRIPT only to a trusted local nano-banana-pro script.

Risk: Setup output may suggest installing uv through a shell installer.

Mitigation: Prefer official package-manager or otherwise verified installation steps for uv before executing installer commands.

## Reference(s):

- [Art Director ClawHub listing](https://clawhub.ai/machinesofdesire/skills/art-director)
- [Publisher profile](https://clawhub.ai/user/machinesofdesire)
- [Project homepage](https://github.com/MachinesOfDesire/art-director)
- [README](artifact/README.md)
- [Aesthetic presets](artifact/presets/README.md)

## Skill Output:

**Output Type(s):** [Files, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated image file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are written as PNG files at requested output paths; generation depends on uv, nano-banana-pro, and GEMINI_API_KEY.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
