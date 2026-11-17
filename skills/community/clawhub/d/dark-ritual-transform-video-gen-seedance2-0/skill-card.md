## Description:

Transforms text briefs or public HTTPS images into short gothic mystery videos with low-key lighting, candles, smoke, a black-gold-crimson palette, and ceremonial motion using WeryAI Seedance 2.0.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoucdr](https://clawhub.ai/user/zoucdr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn ordinary text or image video ideas into short gothic ritual-style clips, then submit the expanded prompt to WeryAI and return playable video links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a WERYAI_API_KEY for paid video generation, and each generation may consume credits.

Mitigation: Use a separate or minimally scoped WeryAI API key where possible, review requests before confirmation, and expect credit usage for retries.

Risk: Prompts and public image URLs are sent to WeryAI API hosts, so confidential prompts or private/internal image URLs could be exposed.

Mitigation: Do not submit confidential prompts, private images, internal URLs, or sensitive user data through this skill.

Risk: The skill instructions require SEEDANCE_2_0, but the bundled CLI does not enforce that model restriction.

Mitigation: Confirm the JSON payload uses model SEEDANCE_2_0 before execution and reject edits that request another model.

## Reference(s):

- [WeryAI video CLI and JSON reference](resources/WERYAI_VIDEO_API.md)
- [ClawHub skill page](https://clawhub.ai/zoucdr/skills/dark-ritual-transform-video-gen-seedance2-0)
- [ClawHub publisher profile](https://clawhub.ai/user/zoucdr)
- [WeryAI video API host](https://api.weryai.com)
- [WeryAI model registry host](https://api-growth-agent.weryai.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with confirmation tables, JSON command payloads, inline video links, or concise error guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, public HTTPS image URLs for image-to-video, and paid WeryAI API access.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
