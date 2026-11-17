## Description:

Destiny Weaver is a turn-based isekai life simulation game engine that generates worlds, characters, yearly events, story records, multi-generation continuation, free actions, and optional scene or character illustrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fslong520](https://clawhub.ai/user/fslong520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to run a Chinese-first interactive life-simulation storytelling game with generated fantasy worlds, character choices, yearly events, persistent saves, story archives, and optional image prompts. It is intended for entertainment and narrative play rather than factual, legal, medical, or financial decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Story state, saves, archives, and image prompts may retain user-entered character or story details locally.

Mitigation: Avoid entering sensitive personal details, and review or remove local saves, story archives, and image prompts before sharing outputs.

Risk: Chinese-first commands and free-form play prompts may be interpreted as game actions when phrasing is ambiguous.

Mitigation: Use clear game-specific phrasing and confirm save, load, export, and image-generation actions before proceeding.

## Reference(s):

- [Fated Codex README](README_EN.md)
- [World Generation Rules](references/world_gen.md)
- [Event System Rules](references/event_system.md)
- [Time System Rules](references/time_system.md)
- [Output Format Specification](references/output_format.md)
- [Character Generation Rules](references/character.md)
- [Novel Generation Rules](references/novel_gen.md)
- [Legacy Continuation Rules](references/legacy.md)
- [Free Action Rules](references/action.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, image prompts, guidance]

**Output Format:** [Markdown gameplay turns and story text, JSON save data, and optional image-generation prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first interactive narrative output with local save and story archive files]

## Skill Version(s):

2.2.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
