## Description: <br>
Perform web searches using the Baidu API, with a focus on Chinese-language content and configurable result counts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leohuang8688](https://clawhub.ai/user/leohuang8688) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Baidu Search from Python or the command line, especially for Chinese-language web, news, research, product, and local search tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search topics, generated requests, and configured API credentials may be sent to external services. <br>
Mitigation: Review provider configuration before use, avoid confidential queries, and install only in environments where external Baidu API use is acceptable. <br>
Risk: Dependencies are specified with minimum versions rather than exact pins. <br>
Mitigation: Pin and review dependency versions before running the skill in sensitive or production environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leohuang8688/bidu-search) <br>
- [Baidu AI Open Platform](https://ai.baidu.com/) <br>
- [Baidu Search API Reference](https://ai.baidu.com/ai-doc/SEARCH) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown-style formatted search results, Python return strings, and CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and returns titles, URLs, and snippets from an external Baidu search API.] <br>

## Skill Version(s): <br>
2.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
