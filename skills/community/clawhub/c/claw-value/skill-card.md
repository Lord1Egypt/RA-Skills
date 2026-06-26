## Description: <br>
OpenClaw capability and value evaluation system that quantifies AI automation usage and generates a playful report with themes, mock-data modes, achievements, and optional poster image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LazyYoun](https://clawhub.ai/user/LazyYoun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to collect local OpenClaw usage signals, evaluate automation depth, and view a local dashboard/API with scores, value estimates, achievements, history, and optional generated poster images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local web app exposes report data without authentication. <br>
Mitigation: Keep the service bound to localhost and do not expose it on untrusted networks. <br>
Risk: The skill reads local OpenClaw logs, installed skill metadata, and configuration summaries, and it saves local history and generated images. <br>
Mitigation: Install only when that local data access is acceptable, and review or remove saved history and generated images as needed. <br>
Risk: Credential handling and clawJudge HTML content need review before broad use. <br>
Mitigation: Provide DASHSCOPE_API_KEY only when image generation is required, and avoid opening untrusted clawJudge links while the service is running. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LazyYoun/claw-value) <br>
- [OpenClaw logging documentation](https://docs.openclaw.ai/zh-CN/logging) <br>
- [Alibaba Cloud Model Studio text-to-image API reference](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference) <br>
- [DashScope multimodal generation endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, HTML, images, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus Flask JSON API responses, an HTML dashboard, and generated PNG image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local Flask service, reads local OpenClaw logs and configuration summaries, and can call DashScope when DASHSCOPE_API_KEY is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
