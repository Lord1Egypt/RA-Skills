## Description:

Claw-Value-Judge is an OpenClaw usage assessment dashboard that quantifies AI automation activity and generates playful value reports with themed views, mock data levels, and gamified achievements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lazyyoun](https://clawhub.ai/user/lazyyoun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to run a local dashboard that summarizes OpenClaw logs, skills, sessions, configuration, automation depth, and estimated usage value. It also provides JSON API endpoints and optional generated image assets for richer reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose local OpenClaw logs, configuration, skill metadata, history, and generated image files if served beyond localhost.

Mitigation: Run it on localhost only unless authentication, access controls, and XSS fixes are added; avoid using --host 0.0.0.0 on shared or public networks.

Risk: Unsafe web handling could let untrusted page input affect the local dashboard experience.

Mitigation: Treat URL-provided report text as untrusted, avoid sharing crafted links, and fix client-side sanitization before broader deployment.

Risk: Image generation may use a credential discovered outside the explicit DASHSCOPE_API_KEY environment variable.

Mitigation: Set DASHSCOPE_API_KEY explicitly for image generation and remove the TOOLS.md credential fallback before broader use.

Risk: Evaluation history and generated images are stored locally without explicit retention or deletion controls.

Mitigation: Use a trusted local environment and add clear retention and deletion controls before using the skill with sensitive activity data.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/lazyyoun/skills/claw-value)
- [OpenClaw logging documentation](https://docs.openclaw.ai/zh-CN/logging)
- [Alibaba Cloud Model Studio text-to-image API](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference)
- [DashScope multimodal generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown setup guidance, local HTML dashboard, JSON API responses, and optional generated image files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a local Flask service and can store evaluation history plus generated images locally.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter declares 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
