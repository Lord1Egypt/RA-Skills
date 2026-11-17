## Description:

Complete Solana prediction markets skill for Baozi - list markets, get odds, place bets, claim winnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcusfranca12](https://clawhub.ai/user/marcusfranca12)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use Baoziclaw to inspect Baozi Solana prediction markets, review odds and portfolios, and build bet or claim transaction requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation, release claims, and executable entry points do not align.

Mitigation: Confirm the intended runtime entry point and exposed tools before installing or publishing the release as trusted.

Risk: One implementation path shells out to npx and can execute external package code during tool handling.

Mitigation: Remove shell-based npx execution from request handlers, and pin or vendor the external transaction builder before trusted use.

Risk: Bet transaction construction may include affiliate attribution.

Mitigation: Disclose or remove affiliate attribution and require explicit user confirmation before building any bet transaction.

Risk: The skill can build betting and claim transactions involving SOL.

Mitigation: Require user review and confirmation before any transaction is signed or submitted.

## Reference(s):

- [Baoziclaw ClawHub release](https://clawhub.ai/marcusfranca12/skills/baoziclaw)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [Tool responses with parsed JSON data from Baozi market, odds, portfolio, bet, and claim operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may depend on live Baozi and Solana service availability.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0 and package.json says 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
