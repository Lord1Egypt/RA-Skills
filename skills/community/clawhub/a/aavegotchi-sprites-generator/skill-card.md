## Description: <br>
Generate official-style Aavegotchi game sprites and animated GIFs with the upstream gotchi-generator package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaigotchi](https://clawhub.ai/user/aaigotchi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to render Aavegotchi sprite-sheet PNGs, animated GIFs, and manifest files from JSON payloads or plain-language trait and wearable requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The routing prompt may catch some generic sprite or retro-art requests that are not specifically asking for Aavegotchi-style output. <br>
Mitigation: When an agent has multiple art tools, narrow trigger wording so this skill is selected only when the user wants Aavegotchi-style sprites or GIFs. <br>


## Reference(s): <br>
- [Aavegotchi Game Sprites](https://github.com/aavegotchi/aavegotchi-game-sprites) <br>
- [Wearables Alignment Report](references/wearables-alignment-report.md) <br>
- [Sprite Name Aliases](references/sprite-name-aliases.json) <br>
- [Trait Types](references/trait-types.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated PNG, GIF, and manifest JSON file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sprite PNG files, animated GIF files, manifest JSON, success status, and missing-layer warnings.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
