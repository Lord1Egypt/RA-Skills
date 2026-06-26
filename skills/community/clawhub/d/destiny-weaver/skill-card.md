## Description: <br>
Destiny Weaver is a turn-based isekai life simulation game engine that generates worlds, characters, life events, story records, save data, and optional scene or character illustrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fslong520](https://clawhub.ai/user/fslong520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and players use this skill to run an AI-driven text adventure that creates an isekai world, advances a character through life stages, records the story, and supports save/load and optional image generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create and retain local game saves, story archives, legacy character data, and generated images. <br>
Mitigation: Avoid entering real secrets or sensitive personal information into character names, story content, or prompts, and review generated local files before sharing or publishing them. <br>
Risk: Broad game-trigger phrases could activate the skill when the user did not intend to start or continue a game. <br>
Mitigation: Use clear game-prefixed commands such as start, continue, save, or load when invoking the skill, and confirm before overwriting or reusing existing saves. <br>


## Reference(s): <br>
- [World Generation Rules](references/world_gen.md) <br>
- [Event System Rules](references/event_system.md) <br>
- [Time System Rules](references/time_system.md) <br>
- [Output Format](references/output_format.md) <br>
- [Character Generation Rules](references/character.md) <br>
- [Novel Generation Rules](references/novel_gen.md) <br>
- [Legacy System Rules](references/legacy.md) <br>
- [Free Action Rules](references/action.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown narrative and structured game-state text, with JSON save data and optional generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local saves, story archives, legacy character data, and optional generated images.] <br>

## Skill Version(s): <br>
2.2.0 (source: server evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
