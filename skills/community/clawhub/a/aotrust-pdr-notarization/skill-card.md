## Description: <br>
Issues a cryptographic proof (PDR) that a digital artifact existed at a specific time by notarizing its SHA-256 hash through AOTrust's external service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gitserge-crypto](https://clawhub.ai/user/gitserge-crypto) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, AI agents, and teams use this skill to create and verify timestamped cryptographic receipts for digital artifacts such as AI outputs, documents, source code, datasets, logs, and audit records without uploading the artifact content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses AOTrust's external notarization service and requires authentication or payment flow integration. <br>
Mitigation: Install only when that external service is intended, and require explicit user approval before sending artifact hashes or starting service calls. <br>
Risk: The production notarization flow involves irreversible USDC payments on Base. <br>
Mitigation: Use a wallet flow that requires manual approval for every payment and confirms the artifact hash, amount, destination, and network before signing. <br>
Risk: An unattended agent with private keys, wallet access, OAuth tokens, or payment authority could submit unintended notarization requests. <br>
Mitigation: Do not give the agent unattended access to private keys or OAuth tokens; keep signing and payment authorization under human-controlled tooling. <br>
Risk: Hashing the wrong bytes can produce a valid PDR for the wrong artifact. <br>
Mitigation: Confirm the exact artifact content before hashing and use deterministic serialization for structured data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gitserge-crypto/skills/aotrust-pdr-notarization) <br>
- [AOTrust MCP endpoint](https://api.aotrust.link/mcp) <br>
- [AOTrust HTTP notarization endpoint](https://api.aotrust.link/notarize) <br>
- [AOTrust PDR verification endpoint](https://api.aotrust.link/v1/pdr/verify) <br>
- [AOTrust web verifier](https://verify.aotrust.link) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides the agent through hashing an artifact, requesting a quote, completing an externally approved payment flow, receiving a PDR, and verifying the result.] <br>

## Skill Version(s): <br>
3.6.2 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
