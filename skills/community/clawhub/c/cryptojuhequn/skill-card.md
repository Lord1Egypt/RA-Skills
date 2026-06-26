## Description: <br>
Crypto Skill provides a read-only API for Feishu crypto-group summaries, contract-address lookup, popular token statistics, KOL analysis, news flashes, and on-chain token data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hengxuZ](https://clawhub.ai/user/hengxuZ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and crypto community analysts use this skill to query crypto group summaries, trace contract addresses through community discussions, inspect token and KOL signals, and retrieve market news through authenticated API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a long-lived Bearer token over unencrypted HTTP to a raw IP address. <br>
Mitigation: Install only if the service operator is trusted, avoid reusing important secrets as the token, avoid untrusted networks, and prefer HTTPS before sensitive use. <br>
Risk: Crypto queries and service-token metadata are shared with a third-party service operator. <br>
Mitigation: Use the skill only when comfortable sharing those queries with the publisher and limit sensitive or personally identifying request content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hengxuZ/cryptojuhequn) <br>
- [API documentation](http://88.222.241.169/static/skill.md) <br>
- [Swagger UI](http://88.222.241.169/docs) <br>
- [Local OpenAPI specification](artifact/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with HTTP and curl examples plus JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only authenticated REST API with a documented daily limit of 500 calls per token.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
