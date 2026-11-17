## Description:

Bilibili Video Downloader helps users resolve Bilibili video links into direct download links and cover image links, with support for single-link or batch processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jessdy](https://clawhub.ai/user/jessdy)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content creators, video collectors, and operations analysts use this skill to turn supported Bilibili URLs into downloadable video and cover links for editing, backup, or offline review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends Bilibili links and the user's API key to yige.zone.

Mitigation: Use only links and credentials that are acceptable to share with that service, and confirm the key can be reset or revoked before use.

Risk: The script can save the API key locally in plaintext when the save-key option is used.

Mitigation: Prefer the YIGE_API_KEY environment variable and avoid saving the key unless local persistence is explicitly acceptable.

Risk: Normal output includes unrelated commercial advertising.

Mitigation: Review generated output before forwarding it to users or downstream systems.

Risk: The skill may be used to download videos the user is not allowed to save.

Mitigation: Use it only for videos the user has rights or permission to download.

## Reference(s):

- [Core Workflow](references/core_workflow.md)
- [Server-Resolved GitHub Source](https://github.com/jessdy/yige-skills/tree/main/skills/bilibili-video-downloader)
- [ClawHub Skill Page](https://clawhub.ai/jessdy/skills/bilibili-video-downloader-3)
- [YigeHub API Key Settings](https://yige.zone/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown tables with direct links by default, or JSON when requested with the script option.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Download links are described by the artifact as short-lived and requiring prompt use.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
