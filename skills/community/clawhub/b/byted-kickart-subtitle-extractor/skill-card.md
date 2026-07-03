## Description: <br>
Extracts existing subtitles from video files through Volcengine/ByteDance cloud services and can return JSON subtitle data or help produce standard SRT subtitles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to upload or reference short MP4/MOV videos, extract embedded or visible subtitles, inspect word-level subtitle timing, and optionally produce SRT subtitle files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests cloud credentials and its own guidance asks users to provide AK/SK values in chat. <br>
Mitigation: Prefer platform-provided API tokens, avoid pasting long-lived secrets into ordinary chat, and use least-privilege credentials that can be rotated after use. <br>
Risk: Videos and media metadata are uploaded to Volcengine/ByteDance cloud services for processing. <br>
Mitigation: Use the skill only for media that may be sent to that service, and avoid submitting confidential or regulated content unless the account and service terms support that use. <br>
Risk: Local media caches and logs may remain under temporary OpenClaw directories after use. <br>
Mitigation: Clear the related /tmp media, output, and log directories after processing sensitive videos. <br>
Risk: Account registration and upgrade-command behavior can affect the user's cloud account or installed skill version. <br>
Mitigation: Review plan registration results and any proposed upgrade command before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/volcengine-skills/byted-kickart-subtitle-extractor) <br>
- [Volcengine Kickart package console](https://console.volcengine.com/kickart/fusion/setting/combobuy?tab=combo) <br>
- [Volcengine IAM access key console](https://console.volcengine.com/iam/keymanage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with shell commands, JSON subtitle files, and optional SRT subtitle text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires cloud credentials and sends video media metadata to Volcengine/ByteDance services.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
