## Description: <br>
Searches Chinese finance communities and portals with Baidu Qianfan web_summary to summarize market sentiment, events, and sector or stock discussions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huangrichao2020](https://clawhub.ai/user/huangrichao2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts can use this skill to run Baidu Qianfan finance searches across sources such as Xueqiu, Zhihu, East Money, and 10jqka for short-term sentiment, event-driven research, and sector rotation analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill disables HTTPS certificate verification while sending a Baidu API key and user queries. <br>
Mitigation: Use only a limited Baidu API key and prefer a fixed version that restores normal HTTPS certificate verification. <br>
Risk: Search queries and message history may contain confidential account data or non-public investment research. <br>
Mitigation: Avoid confidential account data and non-public investment research in queries or message history. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huangrichao2020/baidu-finance-search) <br>
- [Baidu Qianfan web_summary endpoint](https://qianfan.baidubce.com/v2/ai_search/web_summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, API calls, shell commands, configuration] <br>
**Output Format:** [Markdown-style console text followed by summarized JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and accepts JSON parameters for query, sites, time_range, top_k, instruction, and messages.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
