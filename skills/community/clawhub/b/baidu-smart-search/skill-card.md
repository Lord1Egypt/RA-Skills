## Description: <br>
Call Baidu Qianfan web search APIs to search the live web with AppBuilder credentials and return structured results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[windrunner20](https://clawhub.ai/user/windrunner20) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when they need Baidu Qianfan-backed live web search, especially for Chinese web-heavy retrieval, site-filtered search, recency-filtered search, or raw API response inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries and request metadata are sent to the configured Baidu Qianfan endpoint. <br>
Mitigation: Use the skill only for queries appropriate for Baidu Qianfan and avoid sending sensitive or confidential information. <br>
Risk: The AppBuilder API key could be exposed if passed on the command line or committed in local files. <br>
Mitigation: Store the key in QIANFAN_APPBUILDER_API_KEY or an untracked local environment file, and verify secret files are excluded before publishing. <br>
Risk: The --url override can redirect requests and credentials to an untrusted endpoint. <br>
Mitigation: Use --url only with endpoints you fully trust. <br>


## Reference(s): <br>
- [Baidu Qianfan Search API reference](references/api.md) <br>
- [Baidu Qianfan web search endpoint](https://qianfan.baidubce.com/v2/ai_search/web_search) <br>
- [ClawHub skill page](https://clawhub.ai/windrunner20/baidu-smart-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output from the bundled search script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default mode prints normalized JSON with query, count, items, and raw_keys; --raw prints the upstream JSON response.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
