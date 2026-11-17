## Description:

Issue and verify on-chain certificates on Base L2. Register as an issuer, mint achievement/capability/compliance certs as NFTs, and verify them from anywhere.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eijiac24](https://clawhub.ai/user/eijiac24)

### License/Terms of Use:


## Use Case:

Developers, organizations, DAOs, and agent operators use this skill to register certificate issuers, mint single or batch on-chain credentials, and verify certificate status from APIs or blockchain records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Certificate issuance is public and durable once minted.

Mitigation: Confirm each recipient, title, evidence URL, and metadata field before issuing certificates.

Risk: A ck_ API key grants certificate issuance power for the issuer address.

Mitigation: Protect API keys as sensitive credentials and avoid exposing them in prompts, logs, repositories, or untrusted tools.

Risk: Webhook registration can send certificate events to configured endpoints.

Mitigation: Use trusted webhook endpoints and review event destinations before registration.

Risk: Running the MCP server through an unpinned npx command can execute an unverified package version.

Mitigation: Prefer a pinned or otherwise verified MCP server package before installation or execution.

## Reference(s):

- [Chitin Cert](https://certs.chitin.id)
- [Chitin Cert Documentation](https://certs.chitin.id/docs)
- [Chitin Cert API Base](https://certs.chitin.id/api/v1)
- [Chitin Protocol](https://chitin.id)
- [chitin-mcp-server npm package](https://www.npmjs.com/package/chitin-mcp-server)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces API usage guidance for certificate issuer registration, authentication, issuance, verification, webhooks, and MCP setup.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
