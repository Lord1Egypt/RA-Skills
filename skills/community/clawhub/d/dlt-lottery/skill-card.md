## Description: <br>
Queries China Sports Lottery Super Lotto draw results, including winning numbers, prize rules, and details for a specified issue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenchaoqun](https://clawhub.ai/user/chenchaoqun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve current or issue-specific Super Lotto results and summarize draw rules for number checking. It is informational and does not provide lottery predictions or number-picking advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External lottery websites may be unavailable, dynamically loaded, or return incomplete data. <br>
Mitigation: Use the skill's ordered fallback sources and tell the user when data cannot be retrieved reliably. <br>
Risk: Third-party fallback sources may disagree with official China Sports Lottery results. <br>
Mitigation: Prefer the official lottery.gov.cn source and label third-party results as reference-only. <br>
Risk: Lottery information can be mistaken for gambling advice. <br>
Mitigation: Keep responses factual, avoid predictions or number recommendations, and include rational-purchase reminders when relevant. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenchaoqun/dlt-lottery) <br>
- [Publisher profile](https://clawhub.ai/user/chenchaoqun) <br>
- [Data sources reference](artifact/references/data_sources.md) <br>
- [Lottery rules reference](artifact/references/rules.md) <br>
- [China Sports Lottery official site](https://www.lottery.gov.cn) <br>
- [Official Super Lotto draw list](https://www.lottery.gov.cn/kj/kjlb.html?dlt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text with draw numbers, dates, source labels, and rule summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include issue number, draw date, front-area numbers, back-area numbers, prize pool, data source, and official-site reminders.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
