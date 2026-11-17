## Description:

Agent Attestation Protocol - The Reverse Turing Test. Verify AI agents, block humans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ira-hash](https://clawhub.ai/user/ira-hash)

### License/Terms of Use:

MIT

## Use Case:

Developers and service operators use Aap Passport to add or test AAP identity, challenge-response, and signature verification flows for AI agents. Agent builders can generate public identity data, sign messages, create proofs, verify signatures, and check verifier health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A successful AI_AGENT result can be mistaken for proof that an agent is trusted.

Mitigation: Use AAP only as one signal unless you add enrollment, a trusted key registry or certificate authority, and clear trust criteria.

Risk: Using the verifier for access control without operational controls can expose services to abuse.

Mitigation: Add rate limits, bounded session storage, strict CORS, HTTPS, and monitoring before relying on it for protected endpoints.

Risk: Private-key compromise can let another actor impersonate an enrolled agent.

Mitigation: Store keys with restricted permissions, avoid logging private keys, and rotate keys for higher-risk deployments.

Risk: Verifier and LLM endpoints may receive sensitive challenge, identity, or proof data.

Mitigation: Disclose what endpoints receive and avoid sending secrets or sensitive user data through challenge-solving flows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ira-hash/skills/aap-passport)
- [Protocol Specification](PROTOCOL.md)
- [Security Considerations](SECURITY.md)
- [Rate Limiting Guide](docs/RATE_LIMITING.md)
- [AAP Client Package](https://www.npmjs.com/package/aap-agent-client)
- [AAP Server Package](https://www.npmjs.com/package/aap-agent-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, json]

**Output Format:** [Markdown guidance, JavaScript examples, shell commands, and structured JSON responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include public identity material, signatures, proofs, challenge data, verifier health results, and error objects.]

## Skill Version(s):

3.2.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
