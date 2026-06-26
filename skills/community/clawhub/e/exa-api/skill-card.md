## Description: <br>
Exa API integration with managed API key authentication for neural web search, page content retrieval, similar-page discovery, AI-generated answers, and asynchronous research tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call Exa through Maton for web search, content extraction, answer generation with citations, and longer-running research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Maton and linked Exa credentials can grant access to paid search and research APIs. <br>
Mitigation: Store MATON_API_KEY and linked Exa keys as secrets, avoid printing them in logs, and rotate keys if exposed. <br>
Risk: Search, content, answer, and research prompts may disclose private URLs or confidential research topics to external services. <br>
Mitigation: Send only data approved for Maton and Exa, and avoid confidential URLs or prompts unless the workflow permits that exposure. <br>
Risk: Connection create or delete examples can change which Exa API key the gateway uses. <br>
Mitigation: Review connection IDs and confirm create or delete actions before running connection management commands. <br>
Risk: Exa API calls can incur usage costs, especially content extraction and asynchronous research tasks. <br>
Mitigation: Limit result counts, choose research models deliberately, and monitor returned cost fields where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/byungkyu/exa-api) <br>
- [Maton homepage](https://maton.ai) <br>
- [Exa API documentation](https://exa.ai/docs) <br>
- [Exa API reference](https://exa.ai/docs/reference/search) <br>
- [Exa dashboard](https://dashboard.exa.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline JSON, Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Exa connection managed through Maton.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
