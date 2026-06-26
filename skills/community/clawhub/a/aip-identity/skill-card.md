## Description: <br>
AIP Identity helps agents register and verify decentralized identities, sign skills or content, send encrypted messages, and build trust networks with vouches. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[The-Nexus-Guard](https://clawhub.ai/user/The-Nexus-Guard) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to add AIP identity, authentication, signing, encrypted messaging, credential rotation, and trust scoring workflows to AI agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local plaintext private keys can control the user's AIP identity, vouches, signatures, messages, and key rotation. <br>
Mitigation: Use secure registration, keep aip_credentials.json private, and protect the credential file with strict filesystem permissions. <br>
Risk: An untrusted AIP_SERVICE_URL can redirect identity, signing, messaging, or discovery operations to an unintended service. <br>
Mitigation: Use only trusted service URLs and review the configured endpoint before running commands that send identity or message data. <br>
Risk: The security evidence flags messaging reply behavior as requiring review before sensitive replies are sent. <br>
Mitigation: Avoid sending sensitive replies until plaintext reply behavior is clarified or fixed. <br>
Risk: List and trust-graph commands can expose broad discovery information. <br>
Mitigation: Treat discovery output as potentially sensitive and avoid sharing it outside the intended operational context. <br>


## Reference(s): <br>
- [AIP API Reference](references/api.md) <br>
- [AIP Service](https://aip-service.fly.dev) <br>
- [AIP API Docs](https://aip-service.fly.dev/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown with shell commands and JSON credential or API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local credential files and produce signatures, encrypted message payloads, trust graph output, or SVG badge output.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
