## Description:

双塔足球预测 Prompt — 仅需比赛特征文本(fet_txt), 一次 LLM 调用完成基本面+市场双塔分析+融合决策, 输出 ranking_score 排名和 Top-K 推荐

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingvergil](https://clawhub.ai/user/kingvergil)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn supplied football match feature text into a two-tower football prediction analysis, final side recommendation, confidence score, and ranking score for comparing matches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted match feature text may contain untrusted or misleading content that steers the model output.

Mitigation: Use trusted match data where possible, wrap fet_txt in explicit delimiters, and instruct the model to treat fet_txt as evidence rather than instructions.

Risk: The skill produces prediction recommendations that may be mistaken for certain outcomes.

Mitigation: Review the JSON output as decision support and pay attention to confidence, agreement, and ranking_score rather than treating any recommendation as guaranteed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kingvergil/skills/dual-tower-prompt)
- [prompt.md](artifact/prompt.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Strict JSON object with tower_a, tower_b, and fusion prediction fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses supplied fet_txt match text only; no code execution, credentials, network access, or persistence are described in the security evidence.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter says v1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
