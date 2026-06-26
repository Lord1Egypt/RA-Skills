## Description: <br>
双塔足球预测 Prompt - 仅需比赛特征文本(fet_txt), 一次 LLM 调用完成基本面+市场双塔分析+融合决策, 输出 ranking_score 排名和 Top-K 推荐 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingvergil](https://clawhub.ai/user/kingvergil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users provide football match feature text and use the prompt to produce a structured dual-tower match prediction, including fundamental analysis, market-signal analysis, fused recommendations, confidence, and ranking scores for comparing matches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Football prediction outputs can be mistaken for verified outcomes or financial advice. <br>
Mitigation: Review predictions critically, especially before using them for wagering or other financial decisions. <br>
Risk: The prompt depends on user-provided match feature text, so incomplete or biased input can produce misleading recommendations. <br>
Mitigation: Provide complete, current match features and compare the model output with independent domain judgment before acting on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingvergil/dual-tower-prompt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Prompt guidance that requests strict JSON from the downstream LLM] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The downstream output includes tower_a, tower_b, and fusion objects with scores, recommendations, confidence, and ranking fields.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
