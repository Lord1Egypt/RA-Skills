## Description: <br>
家庭消费意图识别 V4 - 智能家庭财务管理，支持收入管理、储蓄目标、消费洞察、定期订阅、趋势分析、购物比价。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wuhaichao87](https://clawhub.ai/user/wuhaichao87) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and households use this skill to classify Chinese natural-language spending intents, record family expenses and income, manage budgets, subscriptions, and savings goals, and generate local finance summaries. It is suited for local personal finance tracking where users are comfortable storing household financial data on their own device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores household expenses, income, budgets, subscriptions, savings goals, and family member profiles as local plaintext JSON files. <br>
Mitigation: Use it only on a trusted device, restrict access to the local data directory, and delete the data directory when the records should no longer be retained. <br>
Risk: Natural-language parsing can misclassify ambiguous spending descriptions before saving records. <br>
Mitigation: Review parsed amount and category values before relying on saved records, budgets, insights, or reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wuhaichao87/family-expense-intent) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Command-line text, JSON records, and Markdown-style reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local plaintext JSON records under ~/.openclaw/skills-data/family-expense-intent/ when users run the bundled Python CLI.] <br>

## Skill Version(s): <br>
4.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
