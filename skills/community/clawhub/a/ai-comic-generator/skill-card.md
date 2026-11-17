## Description:

Create comics, manga and webtoon episodes with the PopNow API: story to page script, character model sheets, consistent panels, speech bubbles with exact text and finished pages or vertical strips. Quotes every page in USD first. Use when the user wants a comic, manga, webtoon, comic strip or illustrated story with recurring characters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyuminjo](https://clawhub.ai/user/kyuminjo)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External creators use this agent skill to turn a story brief into a page script, character model sheets, consistent comic panels, and finished comic pages or vertical webtoon strips through PopNow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Multi-step comic generation spends from a prepaid API USD balance.

Mitigation: Quote the full plan and review its maximum charge before generation; use a dedicated API key with model restrictions and spending caps.

Risk: Prompts, text, and reference media URLs are sent to PopNow and the generation provider, and command parameters may remain in agent logs.

Mitigation: Avoid sensitive personal material, use only rights-cleared references, and check the applicable retention terms when they matter.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kyuminjo/skills/ai-comic-generator)
- [PopNow AI Comic Generator](https://popnow.ai/ai-comic-generator)
- [PopNow API task documentation](https://popnow.ai/docs/tasks)

## Skill Output:

**Output Type(s):** [Text, Images]

**Output Format:** [Comic page scripts and generated comic page or webtoon image links]

**Output Parameters:** [Variable by requested story, format, and page count]

**Other Properties Related to Output:** [May include character model sheets, speech bubbles, and an optional cover; generation is quoted in USD before approval.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
