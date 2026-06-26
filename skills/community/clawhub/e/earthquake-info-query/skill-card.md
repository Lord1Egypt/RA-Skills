## Description: <br>
查询指定时间和区域内的地震信息，支持按震级、时间、深度排序，并返回地震时间、地点、震级和深度等详情。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangpeng258](https://clawhub.ai/user/wangpeng258) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch and summarize earthquake catalog records for China or global scopes, with filters for date range, magnitude, and sorting by time, magnitude, or depth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Earthquake lookups may send query details such as date range, magnitude range, sorting, and China/global scope to CENC. <br>
Mitigation: Invoke the skill only when live earthquake catalog lookup is intended and external CENC requests are acceptable. <br>
Risk: The CENC request can time out or fail, returning a request_error instead of earthquake records. <br>
Mitigation: Treat request_error responses as lookup failures and avoid interpreting them as evidence that no earthquake occurred. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wangpeng258/earthquake-info-query) <br>
- [Publisher profile](https://clawhub.ai/user/wangpeng258) <br>
- [CENC earthquake catalog endpoint](https://www.cenc.ac.cn/prodlaunch-web-backend/open/data/catalogs) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text] <br>
**Output Format:** [Structured JSON result with status, count, earthquake records, or error details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Records include time, location, magnitude, depth, latitude, and longitude when returned by CENC.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
