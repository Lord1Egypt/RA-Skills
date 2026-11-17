## Description:

Create and edit AliExpress product listing images, variant galleries, compatibility graphics, package-content images and multi-country localization bases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, and supporting agents use this skill to generate or edit AliExpress product listing images, variant galleries, compatibility graphics, package-content images, and localized layout bases from approved product references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference uploads can transmit any readable local file supplied with --image or --file to AI Hive.

Mitigation: Use only intentionally selected product media from a dedicated folder, and do not let untrusted prompts choose file paths.

Risk: The API key persistence stores an AI Hive credential under ~/.ai-hive/config.json.

Mitigation: Protect the config file, prefer scoped credentials where available, and rotate the key if the file may have been exposed.

Risk: Generated listing assets may include incorrect product or market claims if prompts, references, or review steps are wrong.

Mitigation: Review outputs against approved SKU facts, localization requirements, certification status, and current platform rules before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/aliexpress-ecommerce-image-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash commands and generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload selected reference media to AI Hive and write generated images to the configured output directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
