## Description:

基于OCR的微信小程序游戏脚本，自动开始游戏、智能选技能、循环刷关支持普通关和精英关。

This skill is ready for commercial/non-commercial use.

## Publisher:

[rascal6666](https://clawhub.ai/user/rascal6666)

### License/Terms of Use:

MIT-0

## Use Case:

Players and automation users can use this skill to run repetitive stages in the PC WeChat mini-program game "向僵尸开炮". It uses OCR to detect game text, start runs, choose skills, handle return screens, and optionally use a monster database for Pro-mode skill recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill captures game-window screenshots and controls the real mouse while PyAutoGUI's corner fail-safe is disabled.

Mitigation: Install it in a dedicated virtual environment, run it as a normal user only while the intended game window is open and visible, and be prepared to terminate the process externally if Ctrl+Q does not work.

Risk: OCR or window-detection mistakes could cause unintended clicks if the wrong window is active or the game state differs from the expected flow.

Mitigation: Confirm the game window title is "向僵尸开炮", manually select the intended stage before running, and monitor initial runs closely.

Risk: The skill writes screenshots and logs locally during operation.

Mitigation: Review and clear generated cache images and log files when they are no longer needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rascal6666/skills/game-autogame)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown instructions with inline shell commands and Python files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local game automation behavior through OCR, screenshots, logs, and mouse clicks against the target game window.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
