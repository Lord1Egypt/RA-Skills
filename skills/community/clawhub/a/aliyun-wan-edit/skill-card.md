## Description:

Use when Alibaba Cloud Model Studio Wan video editing models are needed for style transfer, keyframe-controlled editing, or animation remix workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video workflow builders use this skill to prepare Alibaba Cloud Model Studio Wan edit requests for modifying existing video material through style transformation, keyframe-guided editing, or animation remixing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated request JSON may include video URLs or user content intended for Alibaba Cloud processing.

Mitigation: Review the generated request JSON before sending it to Alibaba Cloud or replacing the example video URL with real user content.

Risk: The helper can create local output files during validation and request preparation.

Mitigation: Run it in an expected workspace path and inspect created files before using them in downstream workflows.

## Reference(s):

- [Alibaba Cloud Model Studio video generation documentation](https://help.aliyun.com/zh/model-studio/video-generation)
- [Alibaba Cloud Model Studio newly released models](https://help.aliyun.com/zh/model-studio/newly-released-models)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON request configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local request JSON file for review before use with Alibaba Cloud.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
