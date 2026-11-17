## Description:

生成 FridayParts Instagram 情绪驱动内容，包括机械圈 Meme、展会动态和 KOL Reel 文案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuxirui677](https://clawhub.ai/user/zhuxirui677)

### License/Terms of Use:

MIT-0

## Use Case:

Social media and marketing teams use this skill to draft FridayParts-branded Instagram meme concepts, event captions, and KOL Reel copy for mechanics, excavator operators, and farmers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad routing triggers may cause general Instagram, meme, or Reel requests to produce FridayParts-branded content.

Mitigation: Enable the skill only where FridayParts Instagram content is desired, and review trigger behavior when multiple skills are installed.

Risk: Generated public social content may miss brand tone, meme quality, or hashtag-count requirements.

Mitigation: Review image text, captions, and hashtags against the bundled output quality checklist before publishing.

Risk: The configured model and creative temperature may affect account cost and output variability.

Mitigation: Confirm the model is acceptable for the account and review outputs before campaign use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhuxirui677/skills/fp-instagram-emotion)
- [README](artifact/README.md)
- [GetClawHub import guide](artifact/docs/如何导入GetClawHub.md)
- [Instagram meme examples](artifact/examples/example_instagram_meme.md)
- [Output quality checklist](artifact/reference/输出质量checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style social copy with meme text suggestions, Instagram captions, and hashtags]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended to be English Instagram copy; meme outputs specify image text, a caption, and 8 hashtags, while KOL Reel outputs require exactly 8 hashtags.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
