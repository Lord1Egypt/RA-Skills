## Description:

Generate children's book illustrations, storybook images, picture-book scenes, and bedtime story art.

This skill is ready for commercial/non-commercial use.

## Publisher:

[632657122](https://clawhub.ai/user/632657122)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through creating age-appropriate children's book visuals. It clarifies the story moment, style, age range, and text-space needs, then prepares prompts and generation commands for WeryAI image output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be persisted in local project or home configuration if setup is run with persistence.

Mitigation: Prefer IMAGE_GEN_API_KEY from the environment, and review permissions on any .image-skills/children-book-image-generator/.env file before use.

Risk: Untrusted batch files, local reference paths, or webhook URLs can expand what data the skill sends to the image gateway.

Mitigation: Use the skill only in trusted projects, avoid untrusted batch inputs and arbitrary webhook URLs, and review reference-image behavior before enabling image-to-image workflows.

Risk: Generated image downloads may require fetching result URLs from the gateway or CDN, including credentialed retry behavior.

Mitigation: Validate result-download origins before sending credentials and inspect failed downloads through the gateway task details instead of resubmitting generation requests.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/632657122/skills/children-book-image-generator)
- [First-Time Setup](references/config/first-time-setup.md)
- [Preferences Schema](references/config/preferences-schema.md)
- [Model Registry Schema](references/config/model-registry-schema.md)
- [Style Presets](references/style-presets.md)
- [WeryAI Gateway Alignment Notes](references/weryai-platform.md)
- [WeryAI API Introduction](https://docs.weryai.com/en)
- [WeryAI Text-to-Image API](https://docs.weryai.com/api-reference/children-book-image-generator/submit-text-to-image-task)
- [WeryAI Image-to-Image API](https://docs.weryai.com/api-reference/children-book-image-generator/submit-image-to-image-task)
- [WeryAI Task Status API](https://docs.weryai.com/api-reference/tasks/query-task-details)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, image files, image URLs]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, generated image files, and image URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses IMAGE_GEN_API_KEY, WeryAI gateway requests, optional reference images, and project or home configuration under .image-skills/children-book-image-generator/.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence; artifact frontmatter declares 0.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
