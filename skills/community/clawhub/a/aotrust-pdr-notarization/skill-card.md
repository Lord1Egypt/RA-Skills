## Description: <br>
Issues a cryptographic proof that a digital artifact existed at a specific time using AOTrust PDR notarization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitserge-crypto](https://clawhub.ai/user/gitserge-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agent operators, and audit workflows use this skill to create and verify PDRs for digital artifacts. It guides agents through reproducible SHA-256 hashing, AOTrust MCP or HTTP API calls, x402 USDC payment on Base, and PDR verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow requires a user-controlled crypto payment authorization. <br>
Mitigation: Use a wallet with limited funds and confirm the recipient, amount, token, and Base network before signing. <br>
Risk: Issued PDRs are immutable and non-refundable. <br>
Mitigation: Confirm the artifact hash and intent to notarize before authorizing payment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitserge-crypto/aotrust-pdr-notarization) <br>
- [AOTrust PDR verification](https://verify.aotrust.link) <br>
- [AOTrust PDR specification](https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr-spec.md) <br>
- [AOTrust PDR parser](https://github.com/GitSerge-crypto/aotrust-skills/blob/main/pdr_parser.py) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with API request examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes hash computation guidance, API endpoints, payment requirements, and verification steps.] <br>

## Skill Version(s): <br>
3.6.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
