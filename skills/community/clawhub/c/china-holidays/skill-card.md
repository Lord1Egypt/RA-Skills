## Description: <br>
China Holidays retrieves and summarizes official Chinese national public holiday schedules, including holiday dates and make-up workdays, for requested years. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xzxiaoshan](https://clawhub.ai/user/xzxiaoshan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer questions about China's official public holiday schedules, make-up workdays, and year-to-year holiday comparisons. It is useful for travel planning, workforce scheduling, and checking whether an official notice has already been cached. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fresh or missing holiday data may require outbound requests to gov.cn and local cache writes inside the skill assets directory. <br>
Mitigation: Use cached yearly notices by default, and refresh only when the user asks for the latest official notice or the requested year is not cached. <br>
Risk: Future-year holiday notices may not be available until the official government notice is published. <br>
Mitigation: When a requested year is unavailable, explain that the official notice may not yet be published and suggest querying an already published year or retrying later. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xzxiaoshan/china-holidays) <br>
- [Official 2026 China holiday notice](https://www.gov.cn/gongbao/2025/issue_12406/202511/content_7048922.html) <br>
- [Official 2025 China holiday notice](https://www.gov.cn/zhengce/zhengceku/202411/content_6986383.htm) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Chinese prose, Markdown tables or lists, or JSON when requested, with shell commands for cache retrieval or refresh.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses cached yearly Markdown notices by default and may fetch from gov.cn when fresh or missing data is requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
