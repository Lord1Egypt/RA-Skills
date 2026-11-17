## Description:

Generates videos with Alibaba Cloud Model Studio DashScope SDK using Wan text-to-video and image-to-video models while normalizing video.generate requests and responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate Alibaba Wan text-to-video or image-to-video assets through DashScope, map normalized video.generate parameters, and save output videos and response evidence for a video-agent pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, reference images, generated URLs, task IDs, logs, images, and videos can be sent to Alibaba DashScope or saved locally.

Mitigation: Use only content approved for DashScope, keep outputs and logs in controlled storage, and remove sensitive artifacts when they are no longer needed.

Risk: The artifact recommends installing dashscope without a pinned version, so SDK behavior or dependency contents can change over time.

Mitigation: Install in a dedicated virtual environment, pin and review the dashscope version before production use, and avoid running as root.

Risk: Video generation is asynchronous and may expose task IDs or generated media URLs during polling and troubleshooting.

Mitigation: Use bounded polling with timeouts, restrict access to task IDs and media URLs, and keep only the logs required for operational troubleshooting.

## Reference(s):

- [DashScope SDK Reference (Wan Video)](artifact/references/api_reference.md)
- [Artifact Source List](artifact/references/sources.md)
- [Alibaba Model Studio Newly Released Models](https://help.aliyun.com/zh/model-studio/newly-released-models)
- [Alibaba Model Studio Text-to-Video Guide](https://help.aliyun.com/zh/model-studio/text-to-video-guide)
- [Alibaba Model Studio First-Frame Image-to-Video Guide](https://help.aliyun.com/zh/model-studio/first-frame-image-to-video)
- [Alibaba Model Studio Model List](https://help.aliyun.com/zh/model-studio/models)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with Python and shell code blocks, JSON request/response shapes, and generated video files when scripts run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DashScope credentials; scripts write videos and optional response logs under output paths such as output/aliyun-wan-video or OUTPUT_DIR.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
