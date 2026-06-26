## Description: <br>
Use A-MAP (Agent Mandate Protocol) to verify incoming agent requests, sign outgoing requests, and delegate permissions to sub-agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmyshuyulee](https://clawhub.ai/user/jimmyshuyulee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to apply A-MAP authorization patterns for agent-to-agent requests, including request verification, request signing, replay prevention, and constrained sub-agent delegation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive signing keys may be exposed or over-privileged. <br>
Mitigation: Use a dedicated least-privilege AMAP_PRIVATE_KEY, store it in environment configuration, and avoid logging private keys or full mandate chains. <br>
Risk: Unpinned package installation may pull an unexpected dependency version. <br>
Mitigation: Verify the npm package source before installation and pin a known-good version. <br>
Risk: Replay protection can fail across multiple instances if nonces are stored only in memory. <br>
Mitigation: Use a shared nonce store such as Redis or Cloudflare KV for multi-instance deployments. <br>
Risk: Delegated agents may receive broader or longer-lived authority than intended. <br>
Mitigation: Keep mandates short-lived, narrowly scoped, and constrained before sending A-MAP headers to trusted services. <br>


## Reference(s): <br>
- [A-MAP Protocol Reference](references/amap-protocol.md) <br>
- [A-MAP Delegation Invariants](references/delegation-invariants.md) <br>
- [A-MAP Error Codes](references/error-codes.md) <br>
- [A-MAP Signed Request Header Format](references/signed-request-format.md) <br>
- [OpenClaw Homepage](https://github.com/Agent-Mandate-Protocol/a-map/tree/main/sdks/typescript/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript examples, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, AMAP_PRIVATE_KEY, and SENDER_PUBKEY for the documented examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
