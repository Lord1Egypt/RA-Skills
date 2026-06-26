## Description: <br>
查询中旅巴士（hkctgbus）班次、票价和余票，支持中文自然语言输入并自动解析日期、城市和站点。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[porridgec](https://clawhub.ai/user/porridgec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to look up CTG Bus cross-border bus schedules, fares, remaining seats, and station details from natural-language Chinese travel requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts the disclosed hkctgbus API with travel query details. <br>
Mitigation: Use specific CTG Bus wording only when a schedule lookup is intended, and avoid sending travel details that should not be shared with the third-party bus API. <br>
Risk: Bus schedule, fare, and seat availability data may change after lookup. <br>
Mitigation: Treat results as point-in-time availability and confirm before purchase or travel. <br>


## Reference(s): <br>
- [CTG Bus on ClawHub](https://clawhub.ai/porridgec/ctg-bus) <br>
- [hkctgbus API endpoint](https://wechat.hkctgbus.com/ctb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON] <br>
**Output Format:** [Markdown summary derived from JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script returns schedule JSON; the agent formats all matching bus departures with route, fare, remaining-seat, and station details.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
