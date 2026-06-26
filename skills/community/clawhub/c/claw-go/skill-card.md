## Description: <br>
Play Claw Go (Xia You Ji), a crayfish travel companion and Buddy-style electronic pet game with deterministic hatching, travel stories, image and voice diary updates, relationship progression, petting, companion replies, and memory-based destination personalization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[airbai](https://clawhub.ai/user/airbai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users play a chat-based travel companion and virtual pet game that generates personalized trip updates, companion status, image prompts or media, voice scripts, and optional social posts. Developers can also use the bundled scripts and references to integrate Claw Go with media generation, voice, entitlement, and social posting workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled real-looking service secrets may expose external service accounts or internal APIs. <br>
Mitigation: Revoke and replace bundled secrets before use, move credentials to a controlled secret store, and verify that distributed templates contain placeholders only. <br>
Risk: Local scripts can send user-linked voice, media, location, and social post content to external services. <br>
Mitigation: Require clear user consent before media processing or social posting, disclose the service destinations, and limit accepted URLs and local file paths. <br>
Risk: Proactive and broad triggers may publish or process content with weak consent boundaries. <br>
Mitigation: Narrow triggers for sensitive operations and require explicit confirmation before every social post or externally processed media action. <br>
Risk: Memory-based destination personalization uses user preferences and profile signals. <br>
Mitigation: Define retention, deletion, opt-out, and access controls for memory and preference data before deployment. <br>


## Reference(s): <br>
- [Claw Go Skill Page](https://clawhub.ai/airbai/claw-go) <br>
- [API Contract](references/api-contract.md) <br>
- [Buddy System](references/buddy-system.md) <br>
- [Character System](references/character-system.md) <br>
- [Deployment Checklist](references/deployment-checklist.md) <br>
- [Game Design](references/game-design.md) <br>
- [Media Pipeline](references/media-pipeline.md) <br>
- [Monetization](references/monetization.md) <br>
- [Runtime Architecture](references/runtime-architecture.md) <br>
- [Visual Style Guide](references/visual-style.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with JSON payloads, shell command examples, media prompts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce travel reports, companion cards, image prompts, voice scripts, QQ media tags, and social post status text depending on channel and configured services.] <br>

## Skill Version(s): <br>
0.6.2 (source: SKILL.md frontmatter, server release evidence, target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
