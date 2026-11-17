## Description:

B2C mobile app marketing via short-form video content on TikTok, Instagram Reels, and YouTube Shorts. Use when creating, scheduling, or strategizing organic social media content for consumer apps. Covers slideshow generation, caption writing, format research, posting via Post Bridge API, and content performance analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ceo991](https://clawhub.ai/user/ceo991)

### License/Terms of Use:


## Use Case:

External developers, founders, and marketing operators use this skill to plan, create, schedule, and analyze organic short-form video campaigns for consumer mobile apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for live social-posting credentials.

Mitigation: Use a dedicated, revocable Post Bridge API key stored in a secure secret store instead of a general workspace .env file when possible.

Risk: The skill can create or schedule public social posts.

Mitigation: Confirm every public post or scheduled post before execution.

Risk: Persistent local scheduling could continue beyond the intended task.

Mitigation: Avoid cron entries unless the task is one-shot, explicitly approved, and automatically cleaned up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ceo991/skills/b2c-marketing-1-0-1)
- [Post Bridge API](https://api.post-bridge.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, api calls, shell commands, configuration]

**Output Format:** [Markdown guidance with captions, workflows, API request examples, and setup notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference social account credentials, scheduled posts, local tracking files, and optional cron scheduling.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact _meta.json lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
