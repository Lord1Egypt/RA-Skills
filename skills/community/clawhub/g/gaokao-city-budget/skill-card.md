## Description: <br>
查询目标城市的大学生活成本，包括房租、餐饮、交通等主要支出，帮助学生和家庭制定大学四年生活预算。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zulirrrr](https://clawhub.ai/user/zulirrrr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, families, and education advisors use this skill to estimate university living costs in Chinese cities, compare city-level cost profiles, and prepare budget reports grounded in cited public sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public cost data can become stale quickly, especially rent and transportation policy data. <br>
Mitigation: Require source platform names, collection dates, and scope notes for figures, and prompt users to verify current listings and official city or school policies. <br>
Risk: Community posts and student anecdotes may not represent typical costs. <br>
Mitigation: Label community sources as reference-only, prefer official or platform data where available, and present ranges rather than absolute judgments. <br>
Risk: Generated HTML budget reports may be mistaken for financial advice. <br>
Mitigation: Include the skill's disclaimer that results are for reference only and are affected by time, location, and personal spending habits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/zulirrrr/gaokao-city-budget) <br>
- [Publisher Profile](https://clawhub.ai/user/zulirrrr) <br>
- [Data Sources Strategy](references/data-sources.md) <br>
- [Output Templates](references/output-templates.md) <br>
- [Search Query Templates](references/search-queries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown answers or local HTML budget reports with cited cost data and disclaimers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [For complete city or multi-city requests, the skill may save HTML reports to an outputs directory; single-expense answers are returned in the conversation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
