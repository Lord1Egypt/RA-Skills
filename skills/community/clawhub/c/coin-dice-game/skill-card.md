## Description: <br>
抛硬币（正/反）和猜骰子大小（大/小）游戏。随机生成结果后发送对应图片。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zx0018](https://clawhub.ai/user/zx0018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can ask an agent to play a simple coin flip or dice-size guessing game and receive a random text result with a matching image path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad trigger phrase such as "玩游戏" could activate the skill when the user did not intend to start this game. <br>
Mitigation: Use explicit phrases such as "抛硬币" or "猜骰子" when invoking the skill. <br>
Risk: Image output may fail or be incomplete if the expected files are not present under assets/. <br>
Mitigation: Install the referenced coin and dice images with the filenames documented by the skill before relying on image responses. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zx0018/coin-dice-game) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [Plain text with MEDIA path lines for matching image assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local random generation and expects referenced image files to exist under assets/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
