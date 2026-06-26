## Description: <br>
游戏自动化-向僵尸开炮 automates a WeChat mini-program game with OCR-driven start, stage-looping, and skill selection for normal and elite stages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rascal6666](https://clawhub.ai/user/rascal6666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and automation users run this skill locally on Windows to automate repeated gameplay in the 向僵尸开炮 WeChat mini-program. It detects game text with OCR, clicks the game window, and can use a monster database to choose recommended skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls the mouse and may click unintended targets if the wrong window is active or the game window is not prepared. <br>
Mitigation: Run it only while the intended game window titled 向僵尸开炮 is open, visible, and selected; stop it with Ctrl+Q when automation is no longer needed. <br>
Risk: The skill captures the game window to ./cache/shot.png and writes local log files during operation. <br>
Mitigation: Use it in a local workspace where those files are expected, and review generated screenshots or logs before sharing the workspace. <br>
Risk: Unpinned Python dependencies may change behavior over time. <br>
Mitigation: Install in a virtual environment and review or pin dependencies before use. <br>
Risk: Pro mode may take a moment to stop after Ctrl+Q. <br>
Mitigation: Allow the running loop to exit cleanly and keep manual control available while testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rascal6666/game-autogame) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Basic README](artifact/README.md) <br>
- [Pro README](artifact/README_PRO.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with Python scripts, dependency configuration, and local runtime guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local game-window automation behavior by controlling the mouse, taking screenshots, reading OCR output, writing logs, and using optional monster data for skill recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
