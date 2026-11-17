## Description:

猫猫表情包技能系统。分析输入文本情绪，从 custom_stickers.json 自动匹配对应表情，支持概率/开关/冷却调节指令。

This skill is ready for commercial/non-commercial use.

## Publisher:

[efgyuhhgy](https://clawhub.ai/user/efgyuhhgy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers can use this skill to add Chinese-language emotion-based sticker selection to chat agents. The skill analyzes message text, selects a matching local sticker image, and supports runtime controls for trigger probability, enablement, and cooldown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Packaged defaults set sticker probability to 1.0 and cooldown to 0, which may add stickers to more responses than expected.

Mitigation: Review sticker_config.json before deployment and adjust probability or cooldown for the intended chat experience.

Risk: Successful sticker matches can return a local absolute sticker path to the caller.

Mitigation: Use relative sticker references where possible and avoid exposing local paths in user-visible responses.

Risk: Bundled sticker images are documented as collected from public internet sources.

Mitigation: Review the packaged sticker set and replace or remove images that do not meet the deployment's content and rights requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/efgyuhhgy/skills/cat-sticker)

## Skill Output:

**Output Type(s):** [text, markdown, configuration]

**Output Format:** [JSON-like Python dictionaries and Markdown-ready sticker references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return local absolute and relative sticker paths, selected emotion, confidence, original message text, and cooldown state.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
