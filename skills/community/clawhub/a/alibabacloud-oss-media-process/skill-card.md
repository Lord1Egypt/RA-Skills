## Description: <br>
Process images, audio, and video files stored in Alibaba Cloud OSS with OSS media processing and IMM features, including transformations, transcoding, detection, metadata extraction, and result delivery as URLs, downloads, or OSS objects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to prepare, transform, inspect, and deliver media assets in Alibaba Cloud OSS without writing direct OSS or IMM integration code. It is suited for thumbnail generation, watermarking, transcoding, audio/video extraction, media metadata checks, and OSS upload/download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate Alibaba Cloud OSS and IMM resources with broad write, processing, admin, and deletion permissions. <br>
Mitigation: Use a least-privilege RAM policy scoped to a dedicated bucket and prefix, avoid granting imm:DeleteProject unless admin cleanup is required, and review auto-setup or lifecycle changes before use. <br>
Risk: Credential material and signed URLs can expose access to Alibaba Cloud resources if printed into transcripts or logs. <br>
Mitigation: Use Aliyun CLI or the SDK default credential chain, do not ask for or print raw credentials, keep output paths inside a workspace directory, and redact presigned URL signing parameters in user-facing text. <br>
Risk: Face, body, and similar media analysis can involve personal or sensitive data. <br>
Mitigation: Use these operations only with appropriate consent, legal basis, and data-handling controls for the media being processed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-oss-media-process) <br>
- [Basic Operations Parameter Reference](references/image-basic-operations.md) <br>
- [IMM Operations Parameter Reference](references/image-imm-operations.md) <br>
- [Video Operations Parameter Reference](references/video-operations.md) <br>
- [Audio Operations Parameter Reference](references/audio-operations.md) <br>
- [IMM Administration](references/imm-admin.md) <br>
- [RAM Permissions](references/ram-policies.md) <br>
- [Media Processing Limitations](references/limitations.md) <br>
- [Common Recipes](references/recipes.md) <br>
- [Common Mistakes and Fixes](references/troubleshooting.md) <br>
- [Alibaba Cloud OSS Media Processing Documentation](https://help.aliyun.com/zh/oss/user-guide/overview-China-site) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local file paths, OSS object paths, redacted signed URLs, request IDs, task IDs, and validation warnings based on executed media operations.] <br>

## Skill Version(s): <br>
0.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
