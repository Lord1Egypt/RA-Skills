## Description:

Generate character design images, original character art, OC portraits, character sheets, and hero concept art.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External users, artists, and developers use this skill to turn character concepts into generated images such as OC portraits, character sheets, mascot designs, and hero concept art through a WeryAI image-generation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary reports that the runtime can upload arbitrary readable local files as reference images.

Mitigation: Use only trusted prompts and batch files, and pass local reference paths only when that exact file is intended for upload.

Risk: The authoritative security summary flags unsafe API-key handling around downloads and persisted key storage on shared machines.

Mitigation: Prefer IMAGE_GEN_API_KEY from the environment and avoid persisted key storage on shared machines.

Risk: The authoritative security guidance recommends using a trusted installed Bun runtime rather than automatic npx execution where possible.

Mitigation: Run the skill with a trusted local Bun installation when available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/632657122/skills/character-image-generator)
- [WeryAI Platform Notes](references/weryai-platform.md)
- [Style Presets](references/style-presets.md)
- [First-Time Setup](references/config/first-time-setup.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Model Registry Schema](references/config/model-registry-schema.md)
- [WeryAI API Introduction](https://docs.weryai.com/en)
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/character-image-generator/submit-text-to-image-task)
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/character-image-generator/submit-image-to-image-task)
- [WeryAI Task Status API](https://docs.weryai.com/api-reference/tasks/query-task-details)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated images and optional project or user configuration under .image-skills/character-image-generator/.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
