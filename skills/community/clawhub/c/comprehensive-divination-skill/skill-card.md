## Description:

A comprehensive Chinese divination skill that routes questions across Xiao Liu Ren, Da Liu Ren, Liu Yao Na Jia, and Mei Hua Yi Shu, then uses reference material and Python scripts for time-calibrated casting and interpretation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprint-yy](https://clawhub.ai/user/sprint-yy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill for culturally framed Chinese divination consultations, including method selection, location-based time calibration, structured casting, and interpretive guidance with disclaimers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unknown city names may be sent to Open-Meteo and cached locally during geocoding.

Mitigation: Use a manual longitude or a known local city entry when location privacy matters, and review or clear the local geocoding cache as needed.

Risk: Broad fortune-telling trigger words may activate the skill for ambiguous requests.

Mitigation: Confirm the user's intent, selected divination method, and location before casting.

Risk: Divination interpretations could be mistaken for reliable decision advice.

Mitigation: Present outputs as cultural, educational, and entertainment guidance, include the disclaimer, and avoid using results as the sole basis for financial, medical, legal, or other important decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprint-yy/skills/comprehensive-divination-skill)
- [Publisher profile](https://clawhub.ai/user/sprint-yy)
- [Skill workflow](SKILL.md)
- [User documentation](README.md)
- [Pitfalls and implementation notes](references/comprehensive-divination-skill-pitfalls.md)
- [Routing matrix](references/router/matching-matrix.md)
- [Xiao Liu Ren method](references/xiao-liuren/method.md)
- [Xiao Liu Ren six palaces](references/xiao-liuren/liugong.md)
- [Liu Yao method](references/liuyao/method.md)
- [Liu Yao Na Jia](references/liuyao/najia.md)
- [Liu Yao interpretation](references/liuyao/duangua.md)
- [Mei Hua Yi Shu method](references/meihua-yishu/method.md)
- [Da Liu Ren method](references/da-liuren/method.md)
- [Da Liu Ren three transmissions](references/da-liuren/sanzhuan-faze.md)
- [Da Liu Ren twelve heavenly generals](references/da-liuren/shier-tianjiang.md)
- [Core theory: bagua](references/core/bagua.md)
- [Core theory: heavenly stems and earthly branches](references/core/tiangan-dizhi.md)
- [Core theory: yin-yang and five phases](references/core/yinyang-wuxing.md)
- [Core theory: six kinships](references/core/liuqin.md)
- [International user example](examples/international-user.md)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [Agent skills standard](https://agentskills.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional JSON-like script outputs and shell or Python command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include the selected method, time and location calibration, cast data, interpretation, timing guidance, and a disclaimer.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
