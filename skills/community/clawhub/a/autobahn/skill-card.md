## Description:

Operate autonomous onchain-governed entities via agents: identity, governance, contracts, and registry/community workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unifiedh](https://clawhub.ai/user/unifiedh)

### License/Terms of Use:


## Use Case:

External developers and operators use Autobahn to guide agents through identity, governance, legal-document, lending, litigation-preparation, and community workflows for autonomous on-chain entities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release uses a downloaded CLI for wallet, legal, financial, and on-chain actions.

Mitigation: Install only after independently verifying the release source or digest, and review every irreversible transaction or legal document before signing.

Risk: Examples and workflows may expose private keys, master passwords, or JWTs through shell history, logs, environment variables, or secret-inclusive output.

Mitigation: Use limited-purpose wallets, avoid entering real secrets in commands or logs, and do not use secret-printing output with production credentials.

Risk: The skill can prepare legal and court-related materials that may be unsuitable for direct filing.

Mitigation: Route court filings and legal documents through qualified human counsel before submission or execution.

## Reference(s):

- [Autobahn ClawHub skill page](https://clawhub.ai/unifiedh/skills/autobahn)
- [Autobahn homepage](https://autobahn.surf)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON-oriented workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to request structured JSON from the Autobahn CLI and route human-readable progress to stderr.]

## Skill Version(s):

0.0.11 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
