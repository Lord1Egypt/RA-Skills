## Description:

Professional image generation assistant for workplace: PPT graphics, marketing posters, product photos, social media content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ximasadila](https://clawhub.ai/user/ximasadila)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and developers use this skill to turn short workplace image requests into professional prompts, call supported image generation platforms, and save generated images for slides, posters, product photos, social media, and related business materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users for provider API keys and may store them in local configuration files.

Mitigation: Use a dedicated secret mechanism or environment variables instead of pasting API keys into chat, and review local provider config files before workplace deployment.

Risk: Workplace prompts may be sent to third-party image providers or search services, especially when grounding/search is enabled.

Mitigation: Avoid confidential customer, product, or business details unless the organization permits those provider and search data flows; disable grounding/search when it is not needed.

Risk: The personal prompt library and local configuration can retain prior request details.

Mitigation: Periodically inspect or delete the saved prompt library and local config files, especially on shared or managed machines.

## Reference(s):

- [ClawHub Easy Image release page](https://clawhub.ai/ximasadila/skills/easy-image)
- [Model selection rules](references/model-selection.md)
- [Professional terminology glossary](references/glossary.md)
- [Platform API configurations](references/platforms/)
- [Scene prompt templates](references/templates/)
- [Jiekou AI documentation](https://jiekou.ai/docs)
- [Google Gemini API documentation](https://ai.google.dev/gemini-api/docs)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance, files]

**Output Format:** [Conversational text with generated image outputs, saved PNG files, configuration JSON, and reusable prompt-library Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call third-party image generation APIs, use grounding/search for current or branded references, save images to a configured local path, and store reusable prompts in a local personal library.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog dated 2026-03-20)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
