## Description:

Generates template-driven emoji videos with Alibaba Cloud Model Studio Emoji from a detected portrait image and selected template ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to prepare and document Alibaba Cloud Model Studio Emoji detect and generation requests for fixed-template facial animation clips from a single portrait image.

### Deployment Geography for Use:

China mainland (Beijing region)

## Known Risks and Mitigations:

Risk: Submitting public portrait image URLs for face-based video generation may expose personal or sensitive face data.

Mitigation: Use only images with appropriate consent and review Alibaba Cloud Model Studio data handling before submitting portrait URLs.

Risk: Provider credentials such as DASHSCOPE_API_KEY or Alibaba Cloud credentials could be mishandled.

Mitigation: Store credentials in environment variables or the documented credentials file, avoid committing secrets, and rotate keys if exposure is suspected.

Risk: Requests may fail or produce unsuitable results if model names, template IDs, detection boxes, or region settings are wrong.

Mitigation: Use the exact documented model names, run detection before generation, choose template IDs from official Alibaba Cloud sources, and operate in the Beijing region.

## Reference(s):

- [Alibaba Cloud Model Studio video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation)
- [Emoji image detection API reference](https://help.aliyun.com/zh/model-studio/emoji-detect-api)
- [Emoji video generation API reference](https://help.aliyun.com/zh/model-studio/emoji-api)
- [Emoji quick start](https://help.aliyun.com/zh/model-studio/emoji-quick-start/)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request payload files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes normalized request payloads under output/aliyun-emoji/ by default and records inputs, detected boxes, template IDs, and polling snapshots for traceability.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
