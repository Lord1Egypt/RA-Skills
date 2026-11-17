## Description:

Send, receive, and manage Bitcoin Lightning payments through Alby Hub's Nostr Wallet Connect, including balance checks and invoice handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiagentkronos-cell](https://clawhub.ai/user/kiagentkronos-cell)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to let an OpenClaw agent send sats to Lightning addresses, pay BOLT11 invoices, and work with Alby Hub through Nostr Wallet Connect. It is suited to controlled payment workflows where wallet permissions and spending limits are configured before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ALBY_NWC_URL grants wallet-spending authority and can expose funds if leaked or reused broadly.

Mitigation: Use a dedicated Alby NWC connection with strict spending limits, store it only in the agent environment, and rotate it immediately if exposure is suspected.

Risk: The package test command runs scripts/wallet.js, which performs live wallet operations rather than a non-spending test.

Mitigation: Do not run npm test for this release; remove scripts/wallet.js or replace it with non-spending checks before trusting the package in an agent workflow.

Risk: Agent-triggered Lightning payments can move real funds to a recipient address or BOLT11 invoice.

Mitigation: Require operator review for recipients and amounts, keep wallet spending limits low, and use the implemented amount and callback validation as a guard rather than as sole approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kiagentkronos-cell/skills/alby-lightning)
- [Publisher Profile](https://clawhub.ai/user/kiagentkronos-cell)
- [Alby Hub](https://albyhub.com)
- [LNURL-pay](https://github.com/lnurl/luds/blob/legacy/lnurl-pay.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Text]

**Output Format:** [Markdown guidance with shell commands and console JSON or text payment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ALBY_NWC_URL and performs live Lightning wallet operations when invoked.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
