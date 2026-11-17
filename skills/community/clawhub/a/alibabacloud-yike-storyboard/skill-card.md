## Description:

Yike Storyboard Creation Skill - Complete AI video creation workflow from novel/script to storyboard via conversational interface.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a novel or script file into a Yike storyboard workflow by confirming parameters, uploading source text, submitting a storyboard job, tracking job status, and opening the resulting storyboard for web-based editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install or update Alibaba Cloud CLI tooling and plugins, including guidance that can make persistent global CLI changes.

Mitigation: Review before installing; prefer trusted package-manager installation, avoid curl-to-bash installation, and do not enable global auto-plugin installation or update unrelated plugins.

Risk: The skill uploads local manuscript or script files to Alibaba Cloud/Yike services for processing.

Mitigation: Confirm the exact resolved file path and content before upload, and assume submitted source material is transmitted to Alibaba Cloud/Yike.

Risk: The workflow uses Alibaba Cloud credentials and cloud permissions.

Mitigation: Use a dedicated, least-privilege Alibaba Cloud RAM user or profile with only the required ICE permissions.

## Reference(s):

- [CLI Installation Guide](references/cli-installation-guide.md)
- [RAM Permission Policies](references/ram-policies.md)
- [Related CLI Commands](references/related-commands.md)
- [Verification Methods](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Alibaba Cloud ICE activation](https://ice.console.aliyun.com/guide/default)
- [Yike AI platform](https://www.yikeai.com/#/home)
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-yike-storyboard)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and generated storyboard URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an Alibaba Cloud account, Aliyun CLI 3.3.3 or later, ICE plugin access, cn-shanghai service configuration, and user-confirmed storyboard parameters before upload.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
