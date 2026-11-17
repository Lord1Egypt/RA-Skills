## Description:

Downloads videos from YouTube, TikTok, Xiaohongshu, Douyin, and similar platforms through a configured external download service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanfeng1234](https://clawhub.ai/user/seanfeng1234)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit supported video URLs, create download tasks through a configured API service, poll status, and receive temporary OSS download links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send video URLs, the configured API key, quota checks, task IDs, and resulting videos to a configurable external service.

Mitigation: Use only a trusted HTTPS download_tool_base_url and avoid private or tokenized video URLs unless sharing them with that service is acceptable.

Risk: The download service can use a paid account balance.

Mitigation: Review balance and pricing before use, and confirm the configured API key belongs to the intended account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seanfeng1234/skills/download-tool)
- [DataMass service](https://www.datamass.cn)
- [Default download API base](https://www.datamass.cn/ai-back)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text status output with a temporary download URL and optional JSON result.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires download_tool_api_key; the default external service returns OSS download links described as valid for 24 hours.]

## Skill Version(s):

1.1.0 (source: server release, SKILL.md frontmatter, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
