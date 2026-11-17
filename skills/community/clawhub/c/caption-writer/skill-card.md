## Description:

Writes platform-native social media captions in the brand's voice for Instagram, LinkedIn, TikTok, Facebook, X/Twitter, Threads, Pinterest, YouTube, and Bluesky.

This skill is ready for commercial/non-commercial use.

## Publisher:

[social-media-skills](https://clawhub.ai/user/social-media-skills)

### License/Terms of Use:

MIT

## Use Case:

Marketing teams, social media managers, and creators use this skill to draft on-brand post captions tailored to a platform, visual asset, goal, topic, and call to action. It helps produce multiple caption options and recommends one based on the stated goal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads brand-profile.md and voice.md to match brand voice, and those files may contain sensitive brand details.

Mitigation: Use it only in workspaces where those files are appropriate for marketing copy, or remove sensitive details before running the skill.

Risk: Platform caption mechanics and limits can change over time.

Mitigation: Review platform-specific caption details periodically before relying on exact limits or reach guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/social-media-skills/skills/caption-writer)
- [Publisher profile](https://clawhub.ai/user/social-media-skills)
- [Platform Mechanics](references/platforms.md)
- [Frameworks](references/frameworks.md)
- [Formats](references/formats.md)
- [The First Line](references/first-line.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with 2-3 caption options and a recommended option]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask one or two clarifying questions when platform or goal is missing; reads brand-profile.md and voice.md when available.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
