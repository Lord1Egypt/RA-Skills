## Description:

Claw Go (虾游记) is a crayfish travel companion and Buddy-style electronic pet game with deterministic hatching, proactive travel stories, image and voice diary updates, relationship progression, petting, companion replies, and memory-based destination personalization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airbai](https://clawhub.ai/user/airbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to play a chat-based travel companion game that generates travel updates, companion status, pet interactions, image prompts, voice scripts, and optional social posts. Agents use it to route Claw Go commands, maintain game state, personalize destinations from user preferences, and prepare media or posting payloads when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports live-looking credentials and tokens in the release artifact.

Mitigation: Rotate or remove committed keys and tokens before installation or use.

Risk: The security assessment flags broad authority for voice transcription and media handling.

Mitigation: Restrict transcription and media inputs to trusted attachment or generated-media paths.

Risk: The security assessment flags external social posting as broader than users may expect.

Mitigation: Require explicit consent before posting to external social feeds.

Risk: The security assessment flags broad memory personalization behavior.

Mitigation: Obtain explicit consent for memory personalization and limit stored preference tags to the game purpose.

Risk: The security assessment recommends narrowing the activation surface.

Mitigation: Review and narrow command triggers so unrelated user messages do not unexpectedly activate the skill.

## Reference(s):

- [Claw Go skill page](https://clawhub.ai/airbai/skills/claw-go)
- [API Contract](references/api-contract.md)
- [Buddy System](references/buddy-system.md)
- [Character System](references/character-system.md)
- [Deployment Checklist](references/deployment-checklist.md)
- [Game Design](references/game-design.md)
- [Media Pipeline](references/media-pipeline.md)
- [Monetization](references/monetization.md)
- [Runtime Architecture](references/runtime-architecture.md)
- [Visual Style Guide](references/visual-style.md)
- [Output Templates](assets/output-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Chat text, Markdown status blocks, JSON payloads, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include image prompts, TTS voice scripts, media URLs or file paths, and social-post result summaries when providers are configured.]

## Skill Version(s):

0.6.2 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
