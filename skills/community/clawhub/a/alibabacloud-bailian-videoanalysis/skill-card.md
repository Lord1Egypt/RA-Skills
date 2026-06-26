## Description: <br>
Alibaba Cloud Bailian Video Analysis uses the Bailian QuanMiaoLightApp API for video comprehension, including shot analysis, ASR transcription, title generation, caption extraction, and mind mapping. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to submit local or URL-hosted videos to Alibaba Cloud Bailian for cloud video analysis, then summarize returned titles, captions, shot analysis, timelines, mind maps, and token usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video content is sent to Alibaba Cloud services and may also be uploaded to OSS with a signed URL. <br>
Mitigation: Install only when this data transfer is acceptable, use a dedicated least-privilege RAM user or temporary role, restrict OSS access to one bucket and the /temp/quanmiao/ prefix, and use the shortest practical signed URL lifetime. <br>
Risk: The skill requires cloud credentials, broad setup steps, and optional automatic CLI plugin installation. <br>
Mitigation: Do not paste credentials into chat or shell history, configure credentials outside the agent session, review CLI plugin behavior before enabling automatic installation, and grant only the permissions listed in the RAM policy guide. <br>
Risk: Uploaded OSS objects and cached task results can retain video URLs, analysis output, or other sensitive details after the task completes. <br>
Mitigation: Delete uploaded OSS objects when finished and remove cached local results under ~/.quanmiao/videoanalysis/ when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-bailian-videoanalysis) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [RAM permissions](references/ram-policies.md) <br>
- [Related commands](references/related-commands.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Bailian Video Analysis activation](https://bailian.console.aliyun.com/cn-beijing#/app/app-market/quanmiao/video-comprehend) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON video analysis results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save raw task results as local JSON under ~/.quanmiao/videoanalysis/ when polling succeeds.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
