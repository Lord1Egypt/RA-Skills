## Description:

Open Source Intelligence (OSINT) tool for researching individuals - professional backgrounds, career timelines, due diligence, competitive intelligence, and investor research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tzannetosgiannis](https://clawhub.ai/user/tzannetosgiannis)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to research public information about people for professional background checks, due diligence, competitive intelligence, investor research, journalism, and credential verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a wallet private key for x402 payment handling.

Mitigation: Use a dedicated low-balance wallet, avoid plaintext key storage when possible, restrict config file permissions, and rotate or move funds if a key may have been exposed.

Risk: The skill executes an unpinned third-party npm package with access to the wallet key.

Mitigation: Review the package before use, run it in a constrained environment, and monitor payment activity from the dedicated wallet.

Risk: People-research outputs can be incomplete, outdated, or misleading.

Mitigation: Treat results as leads for human review and verify important claims against authoritative public sources before making decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tzannetosgiannis/skills/find-people)
- [Publisher profile](https://clawhub.ai/user/tzannetosgiannis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain-text OSINT report returned through shell output, with configuration guidance for payment credentials.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each request costs $0.15 USDC via x402 on Base and may take up to five minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
