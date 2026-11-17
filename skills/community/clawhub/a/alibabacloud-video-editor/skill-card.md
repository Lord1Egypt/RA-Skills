## Description:

Edits and verifies cloud-rendered videos with Alibaba Cloud ICE for timeline composition, normal templates, subtitles, audio mixing, localization, and single-media intelligent-production jobs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and video operations teams use this skill to turn user-supplied media URLs, OSS assets, and upstream analysis into Alibaba Cloud ICE timelines, templates, production jobs, verified playback URLs, and supporting configuration.

### Deployment Geography for Use:

Global, subject to Alibaba Cloud ICE region availability and the selected job region.

## Known Risks and Mitigations:

Risk: Alibaba Cloud credentials may grant broader ICE or OSS access than the task requires.

Mitigation: Use a dedicated least-privileged RAM identity, avoid full ICE/OSS access unless necessary, and prefer short-lived or profile-based credentials.

Risk: Cloud rendering, template creation, and intelligent-production jobs may incur costs and persist outputs or templates.

Mitigation: Confirm region, output bucket, and plan before submission; review persistent OSS and ICE resources after use.

Risk: Long-lived credentials stored in shell startup files or unisolated environments can be exposed.

Mitigation: Avoid storing long-lived keys in startup files where possible and run the skill in an isolated environment with pinned dependencies.

Risk: Verification workflows may leave temporary scratch-frame artifacts.

Mitigation: Keep scratch artifacts in a disposable session directory and clean them after review.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/sdk-team/skills/alibabacloud-video-editor)
- [Skill overview](artifact/SKILL.md)
- [Timeline Basic Structure](artifact/references/01-timeline-basics.md)
- [Output and Job Configuration](artifact/references/08-output-and-job-config.md)
- [Output Verification](artifact/references/11-output-verification.md)
- [Intelligent Production](artifact/references/13-intelligent-production.md)
- [Snapshot and ASR](artifact/references/17-snapshot-and-asr.md)
- [EDL and Compile](artifact/references/18-edl-and-compile.md)
- [Normal Timeline Templates](artifact/references/22-normal-templates.md)
- [RAM Policies](artifact/references/ram-policies.md)
- [Alibaba Cloud ICE API Reference](https://help.aliyun.com/zh/ims/developer-reference/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON timelines, EDL/configuration snippets, shell commands, job IDs, signed playback URLs, and verification notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Alibaba Cloud ICE timeline JSON, normal-template configs, API job commands, and verified output handoff details.]

## Skill Version(s):

0.0.2 (source: server release evidence and artifact/references/manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
