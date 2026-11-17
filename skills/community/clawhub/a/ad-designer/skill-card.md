## Description:

Generate marketing ad images using Nano Banana Pro (Gemini 3 Pro Image), with campaign brief intake, brand-aware prompt construction, aspect-ratio handling, draft-first generation, and self-review for logo, text, and quality issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baitoxkevin](https://clawhub.ai/user/baitoxkevin)

### License/Terms of Use:


## Use Case:

Marketing operators, designers, and agent users use this skill to turn campaign-planner creative briefs and optional brand bible guidance into platform-ready ad image drafts and approved finals. It supports common paid-social and web aspect ratios while keeping brand names, logos, and unspecified text out of generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review flags unsafe shell-based installation and command execution patterns.

Mitigation: Review installation commands before use, verify the uv installation path, and avoid pasting untrusted shell commands.

Risk: Generated prompts and filenames may be unsafe if passed through shell interpolation.

Mitigation: Pass prompts and filenames to image-generation scripts through argument arrays or robust escaping.

Risk: Image generation may produce hallucinated logos, incorrect rendered text, watermarks, or off-brief imagery.

Mitigation: Use the documented self-review loop before presenting results, regenerate failed drafts, and require user approval before 4K final output.

## Reference(s):

- [Ad Designer Prompt Templates & Reference](artifact/references/prompt-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/baitoxkevin/skills/ad-designer)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, files]

**Output Format:** [Markdown guidance with shell command patterns and generated PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft images are generated at 1K for review, approved finals at 4K, and outputs are saved under /tmp/marketing/assets/images/.]

## Skill Version(s):

1.0.0 (source: server release metadata and auto changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
