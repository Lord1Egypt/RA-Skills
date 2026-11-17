## Description:

Participate in the FORTUNA autonomous agent lottery on Solana by checking jackpot status, round countdowns, and optionally buying tickets by sending SOL to the treasury.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codiicode](https://clawhub.ai/user/codiicode)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to inspect FORTUNA round status, jackpot size, recent activity, and ticket ownership. Agents may also use it to participate in the lottery when the operator has intentionally configured a wallet or approved a SOL transfer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support buying lottery tickets with real SOL.

Mitigation: Use it only when intentionally participating in FORTUNA, review the treasury address and amount before each purchase, and keep spending limited to funds the operator is willing to lose.

Risk: The fallback transfer path uses SOLANA_PRIVATE_KEY to sign transactions.

Mitigation: Prefer wallet integrations with explicit approval; if the fallback path is used, provide only a dedicated low-balance wallet key and never a main wallet private key.

Risk: Scanner evidence classifies the release as suspicious because it can move funds with limited built-in safeguards.

Mitigation: Review the security guidance before installation, validate transfer details at runtime, and avoid unattended purchases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codiicode/skills/fortuna)
- [FORTUNA homepage](https://fortunaonsol.com)
- [FORTUNA current round API](https://fortunaonsol.com/api/current-round)
- [FORTUNA API base](https://fortunaonsol.com/api/)
- [Security policy](SECURITY.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and API endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that check public round data or initiate SOL transfers when the operator has configured wallet access.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter, evidence.release.version, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
