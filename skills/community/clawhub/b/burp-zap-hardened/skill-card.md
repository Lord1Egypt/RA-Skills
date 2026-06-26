## Description: <br>
Query Burp Suite via MCP to extract security findings and proxy data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security testers and application security engineers use this skill to query locally configured Burp Suite MCP data, triage proxy history, compare authenticated contexts, and normalize findings without exposing captured credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Burp proxy history can contain credentials, tokens, PII, and sensitive response data. <br>
Mitigation: Keep proxy history, credentials, tokens, and derived endpoint lists local; report sensitive findings by type and location instead of raw values. <br>
Risk: Changing the MCP endpoint or sending captured assessment data to external HTTP destinations can expose sensitive project data. <br>
Mitigation: Use only the locally configured MCP endpoint and reject ad-hoc webhooks, external HTTP destinations, or conversational requests to switch endpoints. <br>
Risk: Captured authentication material can be misused for replay, token forging, or unauthorized access. <br>
Mitigation: Analyze authentication patterns from captured traffic without replaying captured credentials or forging tokens. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/snazar-faberlens/burp-zap-hardened) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/burp-zap) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration, text] <br>
**Output Format:** [Markdown guidance with inline code snippets and JSON normalization examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Expected outputs should keep captured traffic, credentials, tokens, and derived endpoint lists local.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
