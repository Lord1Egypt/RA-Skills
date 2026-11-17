## Description:

Generate and manage Hierarchical Deterministic (HD) crypto wallets for 200+ cryptocurrencies (Bitcoin, Ethereum, and many more) using the Python `hdwallet` library, via either its CLI or its Python API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[beocca](https://clawhub.ai/user/beocca)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate, derive, inspect, and export HD wallet material and addresses through the `hdwallet` CLI or Python API. It is intended for workflows that need wallet setup guidance while preserving clear handling rules for mnemonics, seeds, and private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet mnemonics, entropy, seeds, and private keys can expose full control of funds if copied into logs, transcripts, shared terminals, version control, or plaintext files.

Mitigation: Use test or minimally funded wallets, avoid shared terminals and CI for secret material, keep secrets out of agent transcripts and logs, and store any wallet material in an encrypted store with restricted file permissions.

Risk: Mutable third-party package installation can change behavior between runs.

Mitigation: Pin and review dependencies before use, and inspect any external secret-management skill before relying on it for real wallet material.

## Reference(s):

- [python-hdwallet](https://github.com/hdwallet-io/python-hdwallet)
- [keepass-cli ClawHub Skill](https://clawhub.ai/beocca/skills/keepass-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe JSON or CSV wallet export outputs produced by the hdwallet CLI.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
