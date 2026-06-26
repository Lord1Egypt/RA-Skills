## Description: <br>
Alibabacloud Video Editor generates Alibaba Cloud ICE timeline configurations, submits cloud video editing jobs, polls for completion, and returns final video URLs without requiring local ffmpeg. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media teams use this skill to assemble video timelines for slideshows, multi-clip edits, audio mixing, subtitles, effects, and transitions, then run the edit through Alibaba Cloud ICE. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit billable Alibaba Cloud ICE jobs and use OSS resources. <br>
Mitigation: Use a dedicated least-privilege RAM user or role, confirm the output bucket and path, and review expected charges before submitting jobs. <br>
Risk: Broad Alibaba Cloud permissions can expose more cloud resources than the editing workflow requires. <br>
Mitigation: Prefer the minimum RAM permissions documented for submitting, checking, and retrieving media jobs; use full-access policies only in controlled testing. <br>
Risk: Local media must be uploaded to OSS before editing, which can expose source material if the bucket or object path is misconfigured. <br>
Mitigation: Use an intended OSS bucket and endpoint, verify object access settings, and avoid placing sensitive media in shared output locations. <br>
Risk: The server security guidance notes a missing dependency file should be verified from a trusted source. <br>
Mitigation: Install dependencies only from trusted Alibaba Cloud SDK sources and review package versions before execution. <br>


## Reference(s): <br>
- [Alibabacloud Video Editor skill page](https://clawhub.ai/sdk-team/alibabacloud-video-editor) <br>
- [Timeline Basic Structure](references/01-timeline-basics.md) <br>
- [Multi-Track Audio Mixing](references/02-multi-track-audio.md) <br>
- [Subtitles and Title Effects](references/03-subtitles-and-titles.md) <br>
- [Visual Effects and Transitions](references/04-effects-and-transitions.md) <br>
- [Slideshow Video Template](references/05-slideshow-template.md) <br>
- [Multi-Clip Video Editing](references/06-multi-clip-editing.md) <br>
- [RAM Policies for alibabacloud-video-editor](references/ram-policies.md) <br>
- [RAM User Authorization Documentation](https://help.aliyun.com/zh/ims/user-guide/create-and-authorize-a-ram-user-1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with JSON timeline and output configuration snippets, shell commands, job status text, and final video URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit billable Alibaba Cloud ICE jobs and interact with OSS resources when valid Alibaba Cloud credentials and output configuration are provided.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
