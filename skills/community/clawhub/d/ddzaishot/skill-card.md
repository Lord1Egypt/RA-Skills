## Description: <br>
Ddzaishot supports Dou Dizhu game analysis by scanning visible cards, tracking play state, and returning AI play suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bladezhang](https://clawhub.ai/user/bladezhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Players and agent operators use this skill to analyze Dou Dizhu hands, track visible cards, request suggested plays, and optionally assist with calibrated mouse clicks during gameplay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can capture the visible screen and save screenshots, which may expose sensitive windows or information. <br>
Mitigation: Hide unrelated sensitive windows before scanning, keep the game window focused, and review or delete saved screenshots in the logs directory. <br>
Risk: The skill can automate mouse clicks during gameplay with limited scoping controls. <br>
Mitigation: Use demo and suggestion modes first, calibrate mouse positions carefully, and enable auto mode only when the intended game window is active. <br>
Risk: Card recognition depends on local templates and fixed screen regions, so suggestions may be wrong if recognition is inaccurate. <br>
Mitigation: Create and verify card templates for the target game UI, review scan results before acting, and treat recommendations as advisory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bladezhang/ddzaishot) <br>
- [Publisher profile](https://clawhub.ai/user/bladezhang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, interactive prompts, and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include card lists, gameplay state, recommendations, reasoning text, and mouse calibration coordinates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
