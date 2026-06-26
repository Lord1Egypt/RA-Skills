## Description: <br>
Gets overview and status information from Clarity Protocol, including API capabilities, variant counts, endpoint availability, rate limits, and data freshness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarityprotocol](https://clawhub.ai/user/clarityprotocol) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and researchers use this skill to check Clarity Protocol service status and understand available protein-folding research data before querying or integrating with the API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to clarityprotocol.io. <br>
Mitigation: Install and run it only in environments where outbound access to clarityprotocol.io is acceptable. <br>
Risk: The optional CLARITY_API_KEY is a secret if configured. <br>
Mitigation: Use a scoped or revocable key where possible and keep it in the environment rather than in prompts, logs, or shared files. <br>


## Reference(s): <br>
- [Clarity Fold Status on ClawHub](https://clawhub.ai/clarityprotocol/clarity-fold-status) <br>
- [Clarity Protocol](https://clarityprotocol.io) <br>
- [Clarity Protocol API v1](https://clarityprotocol.io/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text status summary or JSON, with shell command examples in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only HTTP GET requests to Clarity Protocol; optional CLARITY_API_KEY increases the documented rate limit.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
