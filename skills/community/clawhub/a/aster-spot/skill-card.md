## Description: <br>
Aster Spot request using the Aster API. Authentication requires API key and secret key (HMAC SHA256). Supports mainnet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Yuandiaodiaodiao](https://clawhub.ai/user/Yuandiaodiaodiao) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to query Aster Spot market and account endpoints, prepare authenticated HMAC-signed requests, and manage mainnet spot trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through authenticated mainnet exchange actions, including trades, transfers, withdrawals, and API-key creation. <br>
Mitigation: Install only when Aster account operations are intended; use read-only or narrowly permissioned API keys where possible, avoid withdrawal permissions unless required, and require explicit user confirmation for trades, transfers, withdrawals, and API-key creation. <br>
Risk: The skill discusses storing API credentials in files, which can expose secrets if real credentials are committed or shared. <br>
Mitigation: Do not store real secrets in TOOLS.md or repository files; use a secret manager or local environment storage, restrict API keys by IP and permissions, and mask credentials in all agent-visible output. <br>
Risk: Large unfiltered market-data responses can lead to incomplete or misleading analysis if truncated or parsed manually. <br>
Mitigation: Use symbol and limit parameters for targeted requests, summarize broad queries before fetching details, and use jq or structured parsing rather than truncating JSON. <br>


## Reference(s): <br>
- [Aster Spot Authentication](references/authentication.md) <br>
- [Aster Spot Skill Page](https://clawhub.ai/Yuandiaodiaodiao/aster-spot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON examples and shell or Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Aster API request guidance, HMAC signing examples, credential-handling instructions, and JSON response handling guidance.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
