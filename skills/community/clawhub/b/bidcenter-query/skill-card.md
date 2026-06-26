## Description: <br>
查询采招网（bidcenter.com.cn）招标信息，支持按地区、类型、关键词、时间范围筛选。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangpeng258](https://clawhub.ai/user/wangpeng258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to search Bidcenter procurement and tender information by keyword, region, notice type, time range, and page controls. It is intended for users who need structured bid announcements, awards, and related procurement records from bidcenter.com.cn. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search keywords are sent to bidcenter.com.cn. <br>
Mitigation: Avoid using confidential bid strategy, internal supplier details, or sensitive business plans as search keywords unless sharing those queries with Bidcenter is acceptable. <br>
Risk: Bidcenter interface behavior, availability, paid-access coverage, or rate limits may affect result completeness. <br>
Mitigation: Treat returned procurement records as search results to review, and retry later or narrow queries when results are empty, slow, or rate-limited. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangpeng258/bidcenter-query) <br>
- [Bidcenter search](https://search.bidcenter.com.cn/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON] <br>
**Output Format:** [Structured JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns status, listData, total, page, pageSize, and an optional message.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
