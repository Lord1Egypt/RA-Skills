## Description:

抛硬币（正/反）和猜骰子大小（大/小）游戏。随机生成结果后发送对应图片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zx0018](https://clawhub.ai/user/zx0018)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to play a simple Chinese-language coin flip or dice-size guessing game. The skill returns a random text result and points the agent to the corresponding local image asset.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad Chinese trigger "玩游戏" may route general game requests to this skill.

Mitigation: Use the skill for explicit coin-flip or dice-size game requests, or narrow routing rules before deployment.

Risk: The referenced image assets were not included in the inspected artifact files.

Mitigation: Confirm that the expected coin and dice image files exist in the assets directory before enabling image responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zx0018/skills/coin-dice-game)
- [Publisher profile](https://clawhub.ai/user/zx0018)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with image filename or MEDIA path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local random generation and expects matching image assets in an assets directory.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
