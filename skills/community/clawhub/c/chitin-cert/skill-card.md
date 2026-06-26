## Description: <br>
Issue and verify on-chain certificates on Base L2. Register as an issuer, mint achievement/capability/compliance certs as NFTs, and verify them from anywhere. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EijiAC24](https://clawhub.ai/user/EijiAC24) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, agent operators, organizations, DAOs, and individual issuers use this skill to register certificate issuers, mint public on-chain credentials, batch issue certificates, verify certificate status, and integrate certificate notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Issuer API keys can authorize certificate issuance for an issuer address. <br>
Mitigation: Treat ck_ keys as sensitive credentials, do not expose them in prompts or logs, and rotate them if exposure is suspected. <br>
Risk: Wallet private keys or signing authority could be mishandled during issuer registration or API key generation. <br>
Mitigation: Never provide private keys to any service; use wallet signatures only after confirming the exact message, address, and timestamp. <br>
Risk: Certificate records, evidence URLs, and recipient addresses may become public and hard to undo because the workflow uses Base L2 and Arweave. <br>
Mitigation: Manually review certificate text, wallet addresses, evidence links, and expiry values before issuing. <br>
Risk: The optional MCP server is installed and run from npm. <br>
Mitigation: Review the package and its permissions before execution, and run it only in an environment appropriate for credential-handling workflows. <br>
Risk: Webhook endpoints can leak event data or deliver notifications to the wrong system if misconfigured. <br>
Mitigation: Confirm webhook URLs and event subscriptions before registration and monitor receiving systems for unexpected certificate events. <br>


## Reference(s): <br>
- [Chitin Cert Website](https://certs.chitin.id) <br>
- [Chitin Cert Documentation](https://certs.chitin.id/docs) <br>
- [Chitin Cert API Base](https://certs.chitin.id/api/v1) <br>
- [Chitin Cert Skill File](https://certs.chitin.id/skill.md) <br>
- [Chitin Protocol](https://chitin.id) <br>
- [chitin-mcp-server npm Package](https://www.npmjs.com/package/chitin-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, JSON, Configuration] <br>
**Output Format:** [Markdown with curl commands, JSON request and response examples, endpoint references, and MCP setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Certificate issuance requires wallet signatures and issuer API keys; batch issuance supports up to 100 certificates per request.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
