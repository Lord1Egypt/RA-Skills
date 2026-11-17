## Description:

Creates Chinese short-video scripts, spoken scripts, storyboards, titles, cover copy, hashtags, and posting suggestions for Douyin, Bilibili, Xiaohongshu, YouTube, and WeChat Channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, marketers, and social media teams use this skill to draft Chinese-language short-video concepts, scripts, oral narration, storyboards, titles, cover copy, hashtags, and posting suggestions. It is intended for platform-adapted content planning across Douyin, Bilibili, Xiaohongshu, YouTube, and WeChat Channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad content-writing triggers and Chinese-first defaults may activate when a user expected a different language, platform, audience, or tone.

Mitigation: Specify the desired language, platform, audience, tone, and content type in the request, then review the generated copy before publication.

Risk: High-engagement hook and title formulas can produce exaggerated claims if the prompt does not include factual boundaries.

Mitigation: Require truthful claims, provide source facts for product or measurement details, and edit hooks to remove unsupported numbers, urgency, or performance promises.

## Reference(s):

- [Platform Styles](references/platform-styles.md)
- [Script Templates](references/script-templates.md)
- [Hook Formulas](references/hook-formulas.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with Chinese script sections, storyboard tables, titles, cover copy, hashtags, and posting suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first output; when details are missing, the artifact defaults to Douyin, 60-90 seconds, knowledge or review content, ages 18-35, and a light upbeat tone.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
