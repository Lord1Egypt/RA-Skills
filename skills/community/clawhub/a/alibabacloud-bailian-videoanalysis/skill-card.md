## Description:

Alibaba Cloud Bailian Video Analysis Skill for intelligent video comprehension and analysis via the Bailian QuanMiaoLightApp API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to submit videos to Alibaba Cloud Bailian for video comprehension, then retrieve summaries, captions, shot analysis, generated titles, outlines, mind maps, and token usage from the cloud result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may require broad Alibaba Cloud permissions during setup.

Mitigation: Use a dedicated least-privilege RAM user or role and restrict OSS permissions to one approved bucket and the /temp/quanmiao/ prefix.

Risk: Credential exposure could occur if access keys are typed into agent-visible commands or logs.

Mitigation: Configure credentials outside the agent session, never print AK/SK values, and prefer short-lived credentials.

Risk: Local videos are uploaded to Alibaba Cloud for processing.

Mitigation: Review data handling requirements before use and only submit videos approved for Alibaba Cloud processing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sdk-team/skills/alibabacloud-bailian-videoanalysis)
- [Bailian Video Analysis Activation](https://bailian.console.aliyun.com/cn-beijing#/app/app-market/quanmiao/video-comprehend)
- [Bailian Permission Management](https://bailian.console.aliyun.com/cn-beijing?tab=app#/authority)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [RAM Permissions](references/ram-policies.md)
- [Related Commands](references/related-commands.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save completed video-analysis responses as local JSON files and summarize cloud-returned analysis fields.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
