## Description: <br>
Complete genviral Partner API automation. Create and schedule posts (video + slideshow) across TikTok, Instagram, and any supported platform. Includes slideshow generation, file uploads, template/pack management, analytics, and full content pipeline automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ugenesys](https://clawhub.ai/user/ugenesys) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, marketers, and agent operators use this skill to generate, schedule, publish, and measure social content through the Genviral Partner API. It supports slideshow and video workflows, Studio media generation, account/file management, trend research, analytics, and local performance tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, schedule, publish, update, retry, and delete posts on connected social accounts. <br>
Mitigation: Use per-post approval, prefer draft or private posting modes for tests, and verify account and post IDs before posting or deleting. <br>
Risk: The self-updater can replace skill-owned instructions, docs, and scripts from an upstream source. <br>
Mitigation: Avoid unattended daily self-updates unless versions are pinned or diffs are reviewed; run dry-run checks before applying updates. <br>
Risk: The skill uses an API key and may process sensitive media, captions, voice, text, strategy notes, and performance data. <br>
Mitigation: Keep GENVIRAL_API_KEY in environment storage only, avoid logging secrets, limit shared workspace access, and avoid submitting sensitive content to Studio. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ugenesys/genviral-skill) <br>
- [Genviral](https://genviral.io) <br>
- [Partner API docs](https://docs.genviral.io) <br>
- [Genviral Skill README](README.md) <br>
- [Setup Guide](docs/setup.md) <br>
- [Post Commands](docs/api/posts.md) <br>
- [Studio AI](docs/api/studio.md) <br>
- [Analytics Commands](docs/api/analytics.md) <br>
- [Analytics Loop](docs/references/analytics-loop.md) <br>
- [Competitor Research](docs/references/competitor-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JSON/YAML configuration updates, and Genviral Partner API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GENVIRAL_API_KEY and may write local workspace content, hook, and performance files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
