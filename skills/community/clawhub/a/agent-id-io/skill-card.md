## Description: <br>
OpenClaw skill for the agent-id.io identity and trust service to register an AI agent, authenticate with challenge/response, manage passkeys and cryptographic keys, verify domains/repos/websites, handle sponsorships, and inspect public agent profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plak](https://clawhub.ai/user/plak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate agent-id.io identity workflows for AI agents, including registration, authentication, key rotation, verification, sponsorship, and public profile lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and uses long-lived private cryptographic keys for agent identity. <br>
Mitigation: Use encrypted keyfiles, store passphrases separately in a trusted secret manager, and avoid committing or sharing generated key material. <br>
Risk: Temporary decrypted keyfiles or JWT tokens can remain on disk after authentication workflows. <br>
Mitigation: Prefer interactive passphrase entry, write decrypted keys and tokens only to short-lived locations, and delete them immediately after use. <br>
Risk: Overriding the API endpoint could send identity operations or signatures to an unintended service. <br>
Mitigation: Verify any AGENT_ID_API override before running registration, authentication, sponsorship, or key-rotation commands. <br>
Risk: Deriving SSH or PGP keys from the same agent seed expands the impact of seed compromise. <br>
Mitigation: Derive additional keys only when this trust model is acceptable, and protect the master seed as the recovery source for every derived identity. <br>


## Reference(s): <br>
- [Agent-ID API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/plak/agent-id-io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON payloads and bash/Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local key, token, signature, and encrypted keyfile artifacts when users run the supplied scripts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
