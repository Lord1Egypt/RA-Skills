## Description:

Posts or schedules content across Twitter/X, LinkedIn, Facebook, Instagram, TikTok, Threads, Bluesky, Pinterest, and YouTube via the Blotato API with platform-specific content length handling and media upload support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mcbaivn](https://clawhub.ai/user/mcbaivn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content operations teams use this skill to post or schedule social content across multiple connected platforms through Blotato. It helps an agent list connected accounts, adapt content to platform limits, attach media, and submit immediate or scheduled posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A Blotato API key can publish or schedule posts to connected social accounts.

Mitigation: Use a throwaway or narrowly scoped API key where possible, store it in an environment variable or secret manager, and avoid saving it in TOOLS.md.

Risk: Posts, schedules, and media uploads can be submitted without a required final confirmation step.

Mitigation: Require explicit final user confirmation before running any command that posts, schedules, or uploads media.

Risk: Local files supplied as media inputs can be uploaded to Blotato storage.

Mitigation: Review media paths and destination platforms before upload, and only attach files the user explicitly approved.

## Reference(s):

- [Blotato API Reference](references/api.md)
- [Blotato API settings](https://my.blotato.com/settings)
- [ClawHub skill page](https://clawhub.ai/mcbaivn/skills/blotato-post-everywhere)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger external API calls that publish, schedule, or upload media when the user supplies a Blotato API key.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
