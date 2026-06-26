## Description: <br>
Zhipu AI Search lets an agent run web searches through Zhipu AI's Web Search API with selectable engines, recency filters, result counts, content-size options, and domain filters. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[xianglifei](https://clawhub.ai/user/xianglifei) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when an agent needs current web information, news, topic research, or real-time search results from Zhipu-supported search engines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms are sent to Zhipu's external web-search service and could expose sensitive information if entered in queries. <br>
Mitigation: Avoid submitting secrets, private customer data, or proprietary material in search queries. <br>
Risk: The skill requires a Zhipu API key and runs a local Python helper through Bash permissions. <br>
Mitigation: Provide the API key through the ZHIPUAI_API_KEY environment variable, do not hardcode credentials, and scope Bash permissions to the search helper where the agent environment supports it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xianglifei/another-zhipu-web-search) <br>
- [Zhipu Web Search API documentation](https://bigmodel.cn/dev/api/search-tool/web-search) <br>
- [Zhipu BigModel API keys](https://bigmodel.cn/usercenter/apikeys) <br>
- [Zhipu BigModel pricing](https://www.bigmodel.cn/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain-text search summaries, with optional JSON output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search output may include result titles, sources, dates, links, summaries, and optional raw JSON.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
