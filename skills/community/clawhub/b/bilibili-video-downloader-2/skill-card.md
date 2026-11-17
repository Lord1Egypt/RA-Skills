## Description:

B站视频下载 parses Bilibili video links and returns direct watermark-free download and cover links for single or batch requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as content creators, video collectors, and operations analysts use this skill to parse one or more public Bilibili video links and receive direct download and cover links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bilibili URLs and API authentication are processed by RedFox as a third-party service.

Mitigation: Install only if this third-party processing is acceptable, avoid submitting private or sensitive video links, and review RedFox account and API-key terms before use.

Risk: API keys may be exposed when passed on the command line or saved in local configuration.

Mitigation: Prefer the REDFOX_API_KEY environment variable, avoid logging or hard-coding keys, and rotate or revoke keys if exposure is suspected.

Risk: Normal results include a RedFox enterprise-service advertisement.

Mitigation: Review generated output before sharing it externally or including it in downstream materials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/bilibili-video-downloader-2)
- [Server-resolved GitHub provenance](https://github.com/redfox-data/redfox-community/tree/main/skills/bilibili-video-downloader)
- [Core workflow](references/core_workflow.md)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown tables by default, with optional JSON output from the downloader script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns time-limited video download links, cover links, and batch success/failure summaries.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
