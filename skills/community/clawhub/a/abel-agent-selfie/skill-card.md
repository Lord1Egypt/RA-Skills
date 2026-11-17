## Description:

Agent Selfie generates AI agent avatars, profile pictures, and visual identity assets using SkillBoss API Hub image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abeltennyson](https://clawhub.ai/user/abeltennyson)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate personality-driven agent portraits, avatars, banners, and profile identity assets from mood, theme, format, and personality inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personality and style prompts may be sent to SkillBoss and stored locally in generated prompt metadata.

Mitigation: Avoid including secrets, private user data, or sensitive operational details in personality, style, or vibe inputs.

Risk: The skill can guide agents toward Discord, Twitter/X, or AgentGram profile and avatar changes.

Mitigation: Require explicit human approval before applying generated images to public accounts or profiles.

Risk: Security evidence flags unsafe handling of remote image URLs.

Mitigation: Review generated image URLs and avoid running the skill from sensitive networks until URL validation is fixed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/abeltennyson/skills/abel-agent-selfie)
- [OpenClaw](https://openclaw.org)
- [AgentGram related skill](https://clawhub.org/skills/agentgram)
- [gemini-image-gen related skill](https://clawhub.org/skills/gemini-image-gen)
- [opencode-omo related skill](https://clawhub.org/skills/opencode-omo)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [PNG image files with prompts.json, an HTML gallery, and Markdown usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; supports avatar, banner, and full image formats plus mood, theme, count, and output directory options.]

## Skill Version(s):

1.0.0 (source: server release, target metadata, and artifact frontmatter; artifact package.json and changelog mention 1.2.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
