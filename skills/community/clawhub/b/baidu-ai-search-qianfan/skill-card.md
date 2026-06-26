## Description: <br>
Provides Baidu Qianfan web-connected AI search that returns AI-generated answers with source references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k176060444-lgtm](https://clawhub.ai/user/k176060444-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send search questions to Baidu Qianfan and receive AI-summarized answers with citation metadata for web research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu Qianfan using the configured BAIDU_API_KEY. <br>
Mitigation: Avoid submitting secrets, regulated data, or confidential business content unless approved by the organization. <br>
Risk: The skill depends on the Python requests package at runtime. <br>
Mitigation: Confirm the dependency is available before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/k176060444-lgtm/baidu-ai-search-qianfan) <br>
- [Baidu Qianfan AI search endpoint](https://qianfan.baidubce.com/v2/ai_search/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [JSON with an answer, references, request metadata, safety status, and usage details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY and sends user queries to Baidu Qianfan.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
