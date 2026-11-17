## Description:

Generates avatars, profile pictures, PFPs, social media headshots, gaming avatars, and portrait icons.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through creating thumbnail-readable avatars, profile pictures, gaming icons, and personal-brand headshots with WeryAI image models.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, optional reference images, and generated-image metadata are sent to WeryAI.

Mitigation: Use the skill only for content that can be shared with WeryAI, and avoid sensitive personal or confidential material unless that use is approved.

Risk: Security evidence flags under-disclosed local-file upload behavior.

Mitigation: Use public HTTPS reference image URLs and avoid local reference-file paths until the documentation and implementation are aligned.

Risk: The API key can be persisted in local skill configuration.

Mitigation: Prefer IMAGE_GEN_API_KEY from the environment or a protected secret store, and do not commit .image-skills configuration files containing secrets.

Risk: The runtime may rely on an npx -y bun fallback when Bun is unavailable.

Mitigation: Install Bun from a trusted source before use or review the runtime installation path before allowing dependency setup.

## Reference(s):

- [Avatar Image Generator skill page](https://clawhub.ai/632657122/skills/avatar-image-generator)
- [First-Time Setup](references/config/first-time-setup.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Model Registry Schema](references/config/model-registry-schema.md)
- [Style Presets](references/style-presets.md)
- [WeryAI Platform Reference](references/weryai-platform.md)
- [WeryAI API introduction](https://docs.weryai.com/en)
- [WeryAI text-to-image API](https://docs.weryai.com/api-reference/avatar-image-generator/submit-text-to-image-task)
- [WeryAI image-to-image API](https://docs.weryai.com/api-reference/avatar-image-generator/submit-image-to-image-task)
- [WeryAI task status API](https://docs.weryai.com/api-reference/tasks/query-task-details)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell commands, configuration paths, and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a configured WeryAI image model; default aspect ratio is 1:1.]

## Skill Version(s):

1.0.1 (source: server release evidence; packaged SKILL.md frontmatter states 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
