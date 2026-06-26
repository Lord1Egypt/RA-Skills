## Description: <br>
Uses the Baidu Qianfan web search API to retrieve real-time web results for agents that need current facts, news, or verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuhean2021](https://clawhub.ai/user/liuhean2021) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to run Baidu web searches through a configured Qianfan API key and answer current-information questions from structured results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Baidu and may disclose sensitive or private text. <br>
Mitigation: Invoke the skill only when web lookup is intended and avoid placing sensitive or private information in search queries. <br>
Risk: The Baidu Qianfan API key can be exposed if handled outside the dedicated search script. <br>
Mitigation: Store BAIDU_API_KEY in private platform secrets or a protected local config and do not print, log, read aloud, or copy credential values. <br>
Risk: Dependency behavior may drift in controlled environments without a lockfile. <br>
Mitigation: Pin and update dependencies with a lockfile when deploying in managed or audited environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuhean2021/baidu-web-search) <br>
- [Baidu Qianfan API key documentation](https://cloud.baidu.com/doc/qianfan-api/s/Wmbq4z7e5) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON search results with agent-facing guidance for answering from retrieved sources] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires BAIDU_API_KEY or a local config.json apiKey; default result count is 20 and allowed range is 1-50.] <br>

## Skill Version(s): <br>
2.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
