## Description: <br>
Agent Skill for Don't Starve / DST survival guides covering character selection, seasonal preparation, boss strategy, base building, Crock Pot recipes, survival pacing, multiplayer coordination, DLC mechanics, mod recommendations, terminology, lore, and local survivor-profile guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[morandot](https://clawhub.ai/user/morandot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and agent users use this skill to get concise, version-aware Don't Starve and Don't Starve Together guidance for character choices, seasonal preparation, boss fights, base building, recipes, multiplayer coordination, and spoiler-controlled lore. When local file access is available, it can read and update a structured survivor profile so guidance reflects stable gameplay facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain local gameplay facts in survivor-profile.json. <br>
Mitigation: Use DONTSTARVE_MEMORY_DIR to choose the storage location, review or delete the profile when memory is not desired, and avoid storing personal or account information. <br>


## Reference(s): <br>
- [Skill release page](https://clawhub.ai/morandot/dont-starve-skill) <br>
- [Project homepage](https://github.com/morandot/dont-starve-skill) <br>
- [Answer templates](references/answer-templates.md) <br>
- [Style examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional inline shell commands and structured JSON profile patches] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or update a local survivor-profile.json when local file access is available.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
