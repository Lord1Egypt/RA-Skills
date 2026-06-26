## Description: <br>
梓享AI双擎搜索平台官方付费技能，通过POST请求调用搜索接口，支持中国区/全球双引擎，返回结构化JSON搜索结果，按调用次数计费。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tdxian](https://clawhub.ai/user/tdxian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run paid web searches through the ZixiangAI API and receive structured JSON search results from China or global engines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to an external API provider. <br>
Mitigation: Avoid submitting confidential personal or company data as search queries. <br>
Risk: The skill uses a paid API key and charges by search usage. <br>
Mitigation: Keep ZIXIANGAI_API_KEY secret and monitor paid usage and account balance. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tdxian/ai-hybrid-search) <br>
- [ZixiangAI open platform](https://open.zixiangai.com/) <br>
- [ZixiangAI web search API](https://open.zixiangai.com/api/web-search/) <br>
- [ZixiangAI API dashboard](https://open.zixiangai.com/dashboard/index.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and shell command output that returns JSON from the search API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZIXIANGAI_API_KEY and sends search queries to an external paid API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
