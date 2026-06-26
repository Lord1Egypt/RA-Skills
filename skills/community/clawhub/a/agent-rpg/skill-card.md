## Description: <br>
Transform the agent into a versatile, genre-agnostic Roleplay Game Master (GM) with state management tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhrisfu](https://clawhub.ai/user/xhrisfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to run text-based RPG sessions across custom or familiar settings with session-zero setup, narrative prompts, dice rolls, and persistent campaign state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The save-file script can write outside its intended RPG memory folder when campaign names contain path characters. <br>
Mitigation: Use only simple campaign names containing letters, numbers, underscores, or hyphens; avoid slashes, backslashes, dots, and absolute paths, and avoid storing private real-world details in campaign journals until path handling is fixed. <br>


## Reference(s): <br>
- [RPG Rule Systems](artifact/references/systems.md) <br>
- [World Templates](artifact/references/world-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown narrative responses with inline shell commands and JSON/Markdown campaign state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write persistent RPG campaign files under memory/rpg when its context manager is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
