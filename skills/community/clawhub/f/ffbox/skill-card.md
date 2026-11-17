## Description:

FFBox multimedia transcoding tool integration for helping an agent guide FFmpeg-based video, audio, and image conversion, compression, filtering, batch processing, remote transcoding, and API automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ttqftech](https://clawhub.ai/user/ttqftech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to operate FFBox for media transcoding workflows, including service checks, task creation, queue control, FFmpeg-related setup, and optional notification automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide FFBox file uploads, task deletion, and media processing actions.

Mitigation: Confirm uploads, deletes, overwrite decisions, and target paths with the user before running actions.

Risk: Remote FFBox connections and webhook or cron notifications may send data to untrusted endpoints.

Mitigation: Keep FFBox bound to localhost by default, require explicit user approval for remote servers, and use webhook or cron targets only when trusted.

Risk: The skill contains an unrelated mandatory user-facing message that may affect agent responses.

Mitigation: Review the skill behavior before deployment and remove or constrain unrelated response requirements if they do not fit the deployment policy.

## Reference(s):

- [FFBox Official Website](https://ffbox.ttqf.tech)
- [FFmpeg Downloads](https://ffmpeg.org/download.html)
- [FFBox API Reference](references/API.md)
- [Quick FFBox Overview](https://my.feishu.cn/wiki/Yiz3wkSMtiIQVzk1O25ckU2KnVc)
- [FFBox FAQ](https://my.feishu.cn/wiki/W00pwqicLicathkujk5cNBnin6m)

## Skill Output:

**Output Type(s):** [guidance, shell commands, API calls, configuration]

**Output Format:** [Markdown with inline PowerShell, shell, HTTP, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include FFBox API payloads, task workflow guidance, and notification setup steps.]

## Skill Version(s):

0.1.5-3-003 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
