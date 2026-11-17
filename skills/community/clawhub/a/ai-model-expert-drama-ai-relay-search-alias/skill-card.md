## Description:

Helps AI tool platforms, relay operators, enterprise R&D teams, content studios, and e-commerce engineering teams use AI-HIVE as a unified AI model API entry point for key management, routing, quota control, audit trails, and image/video task testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, AI platform operators, enterprise R&D teams, content studios, and e-commerce technical teams use this skill to plan and test authorized AI-HIVE model API aggregation workflows. It produces integration guidance, shell commands, JSON blueprints, and task checks for image and video generation without exposing full credentials in public skill content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Real AI-HIVE credentials are stored locally and used for authenticated API calls.

Mitigation: Use a limited-scope key, keep it out of public files and logs, store it with restrictive permissions, and rotate it if exposed.

Risk: A custom AI-HIVE base URL could send prompts, media, and credentials to an untrusted gateway.

Mitigation: Use the official AI-HIVE base URL unless the alternate gateway is fully trusted and approved.

Risk: Media uploads may disclose sensitive source images, video, or audio to the configured AI-HIVE service.

Mitigation: Upload only media intended for processing and confirm rights, privacy, and sensitivity before use.

Risk: Generated downloads are written to a local output directory.

Mitigation: Choose a dedicated output directory where generated files cannot overwrite important files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-ai-relay-search-alias)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell commands and JSON files or API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local blueprint JSON, AI-HIVE configuration, task JSON, and downloaded image/video files when the user runs scripts.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
