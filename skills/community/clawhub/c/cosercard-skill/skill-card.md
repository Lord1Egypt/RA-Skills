## Description:

Coser 模卡生成工具，帮助用户将多张照片、个人展示信息和风格选项组合成专业的 Cosplay/模特展示卡片。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaosusu](https://clawhub.ai/user/zaosusu)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, cosers, models, photographers, and agents assisting them use this skill to produce image-card generation commands and configuration guidance for cosplay/model casting cards, social posts, previews, and print-ready layouts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes personal photos and optional contact, social, location, and body-measurement details.

Mitigation: Use only consented images and data, run in a controlled workspace, and review generated cards before sharing or publishing.

Risk: The skill automatically records profile-linked usage history and preferences in learning_data.json.

Mitigation: Inspect or clear learning_data.json after use, avoid sensitive profile values when privacy matters, or patch/disable the automatic history write.

Risk: The security summary notes an output path weakness.

Mitigation: Use a dedicated output folder and avoid names or output values containing path separators or '..' when handling untrusted input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaosusu/skills/cosercard-skill)
- [Python documentation](https://www.python.org/)
- [Pillow documentation](https://python-pillow.org/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown or plain text guidance with Python CLI commands; the bundled script writes generated image files such as JPG cards and previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The script supports multiple layout templates, style presets, output sizes, interactive input, batch previews, quick mode, and optional watermarking.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
