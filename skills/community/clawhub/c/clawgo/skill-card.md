## Description:

Play Claw Go, a text-first crayfish travel companion game that runs in chat when explicitly invoked.

This skill is ready for commercial/non-commercial use.

## Publisher:

[airbai](https://clawhub.ai/user/airbai)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke Claw Go to play a text-first companion travel game in chat. The skill produces story beats, status updates, draft postcards, image prompts, voice scripts, and social post captions without publishing externally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may reuse broad long-term memory or infer personal preferences from past chats without clear consent or scoping.

Mitigation: Limit personalization to explicit Claw Go state and provide clear opt-in, correction, and deletion controls for saved preferences.

Risk: Users could mistake generated image prompts, voice scripts, or social captions for completed media or published posts.

Mitigation: Keep media and social outputs clearly draft-only unless the host explicitly provides a real generated or published result.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/airbai/skills/clawgo)
- [Source Homepage](https://github.com/airbai/clawgo/tree/main/skills/claw-go)
- [Game Design](references/game-design.md)
- [Character System](references/character-system.md)
- [API Contract](references/api-contract.md)
- [Visual Style Guide](references/visual-style.md)
- [Monetization](references/monetization.md)
- [Output Templates](assets/output-templates.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown text with structured fields and occasional JSON-style payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Draft-only media and social outputs; no code execution or external publishing in the public registry build.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact declares 0.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
