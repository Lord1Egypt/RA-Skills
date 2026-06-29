## Description: <br>
A Call of Cthulhu 7th Edition Keeper skill that helps an agent prepare scenarios, create and parse character sheets, run gameplay, resolve dice checks, and maintain campaign notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ycqaq233](https://clawhub.ai/user/ycqaq233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and tabletop role-playing players use this skill to have an agent act as a Call of Cthulhu Keeper for scenario preparation, guided play, rule lookups, dice resolution, character management, and session summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads scenario and character files and saves local campaign notes. <br>
Mitigation: Use a dedicated game folder, avoid sensitive personal data in game materials, and delete game_state.md or campaign folders when the retained session data is no longer needed. <br>
Risk: Campaign setup and recovery can interact with existing local folders. <br>
Mitigation: Review prompts before clearing an existing folder and avoid path-like character, module, or scenario names. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ycqaq233/coc-keeper) <br>
- [Publisher profile](https://clawhub.ai/user/ycqaq233) <br>
- [README](artifact/README.md) <br>
- [COC 7th quick rules](artifact/rules/01-quick-rules.md) <br>
- [COC 7th game system](artifact/rules/02-game-system.md) <br>
- [COC 7th combat and chase rules](artifact/rules/03-combat-and-chase.md) <br>
- [COC 7th sanity rules](artifact/rules/04-sanity.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with local file updates and Python command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and updates local campaign notes, character sheets, scenario outlines, scene files, logs, and game state files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and changelog; artifact frontmatter reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
