## Description:

Uses the Zhipu Web Search API to retrieve current, structured web search results with configurable engine, recency, result count, content size, and domain filters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianglifei](https://clawhub.ai/user/xianglifei)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to perform live web searches through Zhipu's Web Search API and return structured search results or readable summaries for current-information tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Zhipu's Web Search API and may include sensitive information if users provide it.

Mitigation: Avoid sensitive or secret search queries, and install only when external API processing of search terms is acceptable.

Risk: The artifact grants broad Python execution and file-write authority beyond the documented search workflow.

Mitigation: Narrow Claude Bash permission to the exact search_util.py command and remove Write unless saved output is required.

Risk: The dependency requirement is not pinned to an exact version.

Mitigation: Pin dependencies for reproducible installs before deployment in controlled environments.

## Reference(s):

- [Zhipu Web Search API documentation](https://bigmodel.cn/dev/api/search-tool/web-search)
- [Zhipu BigModel API keys](https://bigmodel.cn/usercenter/apikeys)
- [Zhipu product pricing](https://www.bigmodel.cn/pricing)
- [ClawHub skill page](https://clawhub.ai/xianglifei/skills/another-zhipu-web-search)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration guidance]

**Output Format:** [Plain text or JSON search results, often summarized in Markdown by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZHIPUAI_API_KEY and sends search queries to Zhipu's Web Search API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
