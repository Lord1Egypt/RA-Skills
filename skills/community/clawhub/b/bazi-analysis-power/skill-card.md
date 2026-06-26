## Description: <br>
Provides structured BaZi chart analysis and fortune-cycle interpretation when a user supplies birth details, a prepared chart, or a specific divination question. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seanding1998](https://clawhub.ai/user/seanding1998) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to produce BaZi chart confirmations, targeted answers, and full structured readings for fortune-cycle questions. It can call a third-party charting API when the user has not provided complete pillars and luck-cycle data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send birth-derived timestamp data and sex to a third-party BaZi charting API. <br>
Mitigation: Require explicit user consent before API-backed chart generation and prefer user-supplied complete chart data when available. <br>
Risk: Personalized readings may include gendered, moral, health, or life-outcome claims from the source material. <br>
Mitigation: Present outputs as divination or interpretive guidance, avoid treating claims as factual advice, and keep health, legal, financial, and life decisions grounded in qualified professional sources. <br>
Risk: API-generated charts may not account for birthplace-based true solar time. <br>
Mitigation: Tell users when API charting was used and recommend cross-checking with a professional charting source or providing complete pillars, luck cycles, and birthplace details. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/seanding1998/bazi-analysis-power) <br>
- [Publisher profile](https://clawhub.ai/user/seanding1998) <br>
- [Yoebao BaZi API](https://yoebao.com/bazi/api/bazi.php) <br>
- [Core rules](references/核心法则.md) <br>
- [Four tombs and storehouses](references/四墓库.md) <br>
- [Earthly branch interactions and twelve growth stages](references/地支互动关系与十二长生.md) <br>
- [Heavenly stem combinations](references/天干五合.md) <br>
- [Peer and rob-wealth rules](references/比劫规则.md) <br>
- [Qiong Tong Bao Jian reference set](references/穷通宝鉴/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown analysis, direct answers, chart confirmations, and optional shell-command-backed charting output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs vary by mode: full analysis, single-question answer, chart confirmation, or clarification request.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
