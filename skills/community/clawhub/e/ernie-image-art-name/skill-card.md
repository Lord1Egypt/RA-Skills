## Description:

Generates artistic text and name-signature images from user-provided names or text using the Baidu AI Studio ERNIE-Image API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whisky-12](https://clawhub.ai/user/whisky-12)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to turn names or short text into stylized typography, calligraphy, cartoon signature, and watercolor-pencil signature images. It guides token setup, style selection, image generation, and local result handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a long-lived Baidu AI Studio bearer token.

Mitigation: Use the AISTUDIO_ACCESS_TOKEN environment variable when possible and rotate the token if it may have been exposed.

Risk: Using --token or --set-token can leave credentials in shell history, logs, or config.json.

Mitigation: Avoid storing the token in the skill directory and remove or rotate credentials after use.

Risk: Generated image files are written to a local output directory.

Mitigation: Choose a user-controlled output folder and review generated files before sharing or publishing them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/whisky-12/skills/ernie-image-art-name)
- [Baidu AI Studio Access Token](https://aistudio.baidu.com/account/accessToken)
- [Baidu AI Studio ERNIE-Image API Reference](artifact/references/api_docs.md)
- [Baidu AI Studio Images Generations Endpoint](https://aistudio.baidu.com/llm/lmapi/v3/images/generations)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline shell commands and locally saved PNG image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated images are saved to a user-selected or configured local output directory.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; artifact frontmatter version is 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
