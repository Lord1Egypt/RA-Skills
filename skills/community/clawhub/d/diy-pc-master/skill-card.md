## Description: <br>
diy-pc-master helps users generate custom PC build recommendations, query parts from DIYZP.cn, and assess hardware compatibility for budgets and use cases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangzbin90-source](https://clawhub.ai/user/huangzbin90-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and PC builders use this skill to request budget-based desktop PC configurations, retrieve matching component options, and receive compatibility notes before considering a build. <br>

### Deployment Geography for Use: <br>
Global; practical purchase-link coverage depends on DIYZP.cn and JD availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a hardcoded shared token and raw SQL queries against DIYZP.cn. <br>
Mitigation: Install only where contacting DIYZP.cn is acceptable; the publisher should move the token out of the skill text and keep the API limited to safe read-only product lookups. <br>
Risk: Generated recommendations can include JD purchase links that may be monetized. <br>
Mitigation: Review links before use and require clear disclosure if links are affiliate or otherwise monetized. <br>
Risk: Part availability, prices, and compatibility guidance depend on external data and model reasoning. <br>
Mitigation: Treat recommendations as reference material and independently verify component compatibility, prices, and availability before purchase. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huangzbin90-source/diy-pc-master) <br>
- [DIYZP.cn SQL API endpoint](https://www.diyzp.cn/api/sql_api.php) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, SQL queries, API calls, Guidance] <br>
**Output Format:** [Markdown recommendations with JSON SQL query snippets, compatibility notes, and purchase links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JD purchase links and a DIYZP.cn data-source note.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
