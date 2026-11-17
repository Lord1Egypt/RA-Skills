## Description:

Use when generating talking, singing, or presentation videos from a single character image and audio with Alibaba Cloud Model Studio digital-human model `wan2.2-s2v`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to prepare Alibaba Cloud Model Studio requests for image-and-audio driven digital-human video generation, including detection and generation payloads for talking, singing, or presentation clips.

### Deployment Geography for Use:

China mainland (Beijing region)

## Known Risks and Mitigations:

Risk: Public image and audio URLs may expose source media to Alibaba Cloud provider processing.

Mitigation: Use only media you are authorized to submit, avoid sensitive inputs, and confirm provider data-handling requirements before running the workflow.

Risk: The skill requires DASHSCOPE_API_KEY or Alibaba Cloud credentials for provider use.

Mitigation: Store credentials outside the skill files, scope access appropriately, and avoid committing generated request evidence that includes secrets.

Risk: Generated digital-human videos can misrepresent a person if the source image or audio is unauthorized.

Mitigation: Use consented image and audio inputs and review generated video before publication or distribution.

## Reference(s):

- [Alibaba Cloud Model Studio video generation overview](https://help.aliyun.com/zh/model-studio/use-video-generation)
- [Alibaba Cloud wan2.2-s2v video generation API reference](https://help.aliyun.com/zh/model-studio/wan-s2v-api)
- [ClawHub skill page](https://clawhub.ai/cinience/skills/aliyun-wan-digital-human)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON request files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes normalized request payloads under output/aliyun-wan-digital-human/ by default.]

## Skill Version(s):

1.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
