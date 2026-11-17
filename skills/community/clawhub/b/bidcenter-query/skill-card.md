## Description:

查询采招网（bidcenter.com.cn）招标信息，支持按地区、类型、关键词、时间范围筛选

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangpeng258](https://clawhub.ai/user/wangpeng258)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting Chinese procurement research use this skill to query bidcenter.com.cn tender and award records by keyword, region, notice type, time range, and pagination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad procurement-related prompts may activate the skill and send search keywords, region, type, time range, page, and page size to bidcenter.com.cn.

Mitigation: Use this skill only for intended bidcenter.com.cn tender searches and avoid confidential or sensitive search terms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangpeng258/skills/bidcenter-query)
- [bidcenter.com.cn search](https://search.bidcenter.com.cn/)
- [bidcenter.com.cn search API endpoint](https://interface.bidcenter.com.cn/search/GetSearchProHandler.ashx)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Text]

**Output Format:** [JSON object containing status, listData, total, page, pageSize, and optional message fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns bid records with titles, types, URLs, dates, locations, budget or award amounts, project stage, purchase method, and project flags when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
