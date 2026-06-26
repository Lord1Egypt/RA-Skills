## Description: <br>
Real-time web search powered by Alibaba Cloud Bailian (DashScope) MCP service for latest news, current events, and facts that may have changed recently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zengxi](https://clawhub.ai/user/zengxi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external users use this skill to let an agent retrieve real-time web search results through Alibaba Cloud Bailian's DashScope MCP service. It is intended for current information requests such as news, recent announcements, and other time-sensitive facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and the DashScope API key are sent to Alibaba Cloud during use. <br>
Mitigation: Use only approved DashScope credentials and avoid submitting secrets, regulated personal data, or confidential business details unless that use is approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zengxi/bailian-search) <br>
- [Alibaba Cloud Bailian Console](https://bailian.console.aliyun.com) <br>
- [DashScope Documentation](https://help.aliyun.com/document_detail/611474.html) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Console text with search result titles, URLs, and snippets; Markdown guidance in documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, python3, and the DASHSCOPE_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, package.json, README, and skill documentation) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
