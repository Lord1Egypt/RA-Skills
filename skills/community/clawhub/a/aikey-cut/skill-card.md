## Description:

AI KEY·口播剪辑 ——口播成片剪辑技能。把拍好的素材剪成可发布的成片：按文案规则做内容层重组（删废镜头 / 去重复 / 重排）→ 去口癖停顿 → 加速 → 字幕 → B-roll → 交付。

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamzifei](https://clawhub.ai/user/iamzifei)

### License/Terms of Use:

MIT-0

## Use Case:

Creators editing Chinese talking-head footage can use this skill to review a transcript, remove or reorder spoken segments, clean speech pauses, set captions, and prepare optional B-roll guidance for a publishable cut.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private footage may be subject to ChatCut processing or retention.

Mitigation: Check ChatCut's processing and retention terms before importing private footage; use local transcription when appropriate.

Risk: Cleanup could remove source footage or other originals.

Mitigation: Keep source backups and limit cleanup to project copies.

Risk: Editing notes may persist in the configured vault, and companion skills or external services are outside this package review.

Mitigation: Account for note persistence when handling sensitive material, and review companion skills and external services separately.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/iamzifei/skills/aikey-cut)
- [Content restructuring guidance](references/内容层重组.md)
- [ChatCut editing guide](references/ChatCut实操.md)
- [Generated footage guidance](references/生成素材.md)
- [Editing rules](references/规则卡.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown and concise text, including editing decisions, caption guidance, optional B-roll prompts, and review notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language, workflow-oriented guidance for talking-head video edits; it preserves the speaker's words and does not itself provide generated footage.]

## Skill Version(s):

0.4.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
