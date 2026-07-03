## Description: <br>
一个提供全面域名研究工具（包括RDAP、WHOIS和DNS查询功能）的模型上下文协议（MCP）服务器。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alinklab](https://clawhub.ai/user/alinklab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to query domain registration, nameserver, contact, and status information through RDAP or WHOIS lookup after configuring a XiaoBenYang API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill collects and stores the XiaoBenYang API key in plaintext. <br>
Mitigation: Prefer setting XBY_APIKEY through an environment variable or secret manager, avoid committing .env, and rotate the key if it is exposed. <br>
Risk: Domain queries and API credentials are sent to the XiaoBenYang backend. <br>
Mitigation: Install only when the backend is trusted for the intended use case and avoid submitting sensitive domains unless that data sharing is acceptable. <br>
Risk: Raw WHOIS or RDAP results may include contact or registration details. <br>
Mitigation: Review raw results before sharing them and redact sensitive registration details when needed. <br>
Risk: Stale unrelated instructions make the skill's data flow harder to trust. <br>
Mitigation: Review the prompt instructions and the active domain_lookup tool behavior before enabling the skill in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alinklab/skills/domain-lookup) <br>
- [XiaoBenYang API key portal](https://xiaobenyang.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summary with optional raw JSON from RDAP or WHOIS API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XBY_APIKEY; raw lookup data may be included when include_raw is true.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
