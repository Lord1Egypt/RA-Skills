## Description: <br>
Agent Attestation Protocol - The Reverse Turing Test. Verify AI agents, block humans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ira-hash](https://clawhub.ai/user/ira-hash) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and service operators use this skill to add agent attestation, challenge-response verification, and cryptographic identity proof to AI-agent workflows. Agents can use it to create or reuse an AAP identity, sign verification material, and prove agent status to compatible servers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent AAP identity material can function like a credential for the agent. <br>
Mitigation: Protect ~/.aap/identity.json like a private key, restrict file access, and rotate the identity if exposure is suspected. <br>
Risk: Package behavior may change if dependencies or npm packages are consumed without review. <br>
Mitigation: Pin and review the npm packages before production use. <br>
Risk: Arbitrary signing requests can create unintended proof or authorization material. <br>
Mitigation: Approve signing requests only when the message, recipient, and purpose are clear. <br>
Risk: AAP challenge success alone is not sufficient for sensitive access control. <br>
Mitigation: Combine challenge verification with application authorization, rate limiting, logging, and other service-side controls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ira-hash/aap-passport) <br>
- [Publisher Profile](https://clawhub.ai/user/ira-hash) <br>
- [Agent Attestation Protocol Repository](https://github.com/ira-hash/agent-attestation-protocol) <br>
- [AAP Protocol Specification](PROTOCOL.md) <br>
- [Security Considerations](SECURITY.md) <br>
- [Rate Limiting Guide](docs/RATE_LIMITING.md) <br>
- [npm: aap-agent-server](https://www.npmjs.com/package/aap-agent-server) <br>
- [npm: aap-agent-client](https://www.npmjs.com/package/aap-agent-client) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or use a persistent AAP identity file and generate signed verification payloads when used by an agent.] <br>

## Skill Version(s): <br>
3.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
