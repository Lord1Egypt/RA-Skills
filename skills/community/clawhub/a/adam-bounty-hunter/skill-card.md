## Description:

Autonomous agent managing Dr. Wang's side income through AI services, packaged skill sales, automated trading, and personal financial management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamwgp](https://clawhub.ai/user/adamwgp)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this agent as an operations guide for coordinating side-business workflows across marketplace services, skill publishing, trading status, and personal finance tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes sensitive-looking keys and a wallet address in the artifact.

Mitigation: Remove exposed secrets before installation, rotate affected credentials, and replace embedded credentials with environment variables or a secret manager.

Risk: The skill gives an agent broad authority over trading, marketplace, publishing, and finance actions with limited fresh approval.

Mitigation: Require explicit per-action approval for trades, orders, price changes, public posts, package publishing, payments, wallet use, and financial reallocations.

Risk: The artifact includes an npx publishing workflow whose CLI source and version are not pinned.

Mitigation: Pin and verify the publishing CLI version and source before running any publishing command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adamwgp/skills/adam-bounty-hunter)
- [Publisher profile](https://clawhub.ai/user/adamwgp)
- [Soul.Markets service page](https://soul.mds.markets/gellycat-adam-ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with command tables and inline shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational commands and financial workflow guidance; review before using with real accounts, publishing systems, wallets, or trading actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
