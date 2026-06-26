## Description: <br>
数字宠物是一个可爱的 3D 拉布布（Labubu）数字宠物，支持互动喂食、玩耍、抚摸，可用于桌面宠物陪伴、3D 互动展示和宠物养成游戏。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[WittFan](https://clawhub.ai/user/WittFan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to run a local 3D digital pet experience with feeding, play, petting, mouse-following animation, sound feedback, and an optional desktop widget. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local visual pet demo loads Three.js from a public CDN. <br>
Mitigation: Use it on a trusted network; bundling Three.js locally or adding SRI would reduce supply-chain risk. <br>
Risk: The skill starts a local HTTP server for the browser demo. <br>
Mitigation: Stop the local server when finished. <br>
Risk: The optional desktop widget runs as a local tray application. <br>
Mitigation: Use the tray Quit option for the desktop widget when finished. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/WittFan/digital-pet) <br>
- [Publisher profile](https://clawhub.ai/user/WittFan) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Files, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with HTML, JavaScript, CSS, Python files, and local shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local browser-based Three.js pet and optional PyQt desktop widget; no API keys were detected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
