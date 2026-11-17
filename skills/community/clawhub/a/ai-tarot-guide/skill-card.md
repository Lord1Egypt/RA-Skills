## Description:

AI塔罗指引 helps Chinese-speaking users explore tarot questions, card meanings, spreads, tarot systems, psychology-oriented reflection, and ethical boundaries, with optional interactive HTML reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bettermen](https://clawhub.ai/user/bettermen)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking users and assistants use this skill for tarot self-reflection, card interpretation, spread-based readings, and learning about tarot history, systems, methods, psychology, and ethics. The skill frames readings as self-exploration rather than deterministic prediction or professional advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML reports may load Chart.js from a CDN, which can be unsuitable for sensitive personal details.

Mitigation: Avoid entering sensitive personal information into reports that execute third-party JavaScript, or generate charts with local CSS, SVG, or canvas instead.

Risk: Tarot readings may be misused as deterministic predictions or as substitutes for medical, legal, financial, or crisis support.

Mitigation: Keep readings framed as self-reflection, limit predictions to the documented three-month scope, and direct users to qualified professionals for medical, legal, financial, self-harm, or crisis concerns.

## Reference(s):

- [塔罗职业伦理（Ethics）](references/ethics.md)
- [大阿卡纳（Major Arcana）— 22张详解](references/major-arcana.md)
- [小阿卡纳 — 圣杯组（Cups / Chalices）](references/minor-arcana-cups.md)
- [小阿卡纳 — 星币组（Pentacles / Coins / Disks）](references/minor-arcana-pentacles.md)
- [小阿卡纳 — 宝剑组（Swords）](references/minor-arcana-swords.md)
- [小阿卡纳 — 权杖组（Wands / Rods）](references/minor-arcana-wands.md)
- [读牌方法 — 五维解读框架](references/reading-methods.md)
- [塔罗牌阵详解（Spreads）](references/spreads.md)
- [塔罗历史 — 三大体系](references/tarot-history.md)
- [塔罗与心理学](references/tarot-psychology.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown responses with optional single-file HTML, CSS, and JavaScript reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language tarot guidance; generated HTML reports may use Chart.js from a CDN when charting is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
