## Description: <br>
Send, receive, and manage Bitcoin Lightning payments through Alby Hub's Nostr Wallet Connect, including balance checks and invoice handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiagentkronos-cell](https://clawhub.ai/user/kiagentkronos-cell) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an OpenClaw agent send sats to Lightning addresses, pay BOLT11 invoices, check balances, and create receive invoices through an Alby Hub NWC connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A spend-capable Alby NWC connection can move wallet funds when payment commands run. <br>
Mitigation: Use a dedicated wallet connection with strict spending limits, and verify recipient, invoice, and amount before invoking payment commands. <br>
Risk: The NWC URL contains wallet secret material and can allow spending if exposed. <br>
Mitigation: Store the URL only in environment configuration, never commit or share it, and rotate it immediately if exposure is suspected. <br>
Risk: The package test command executes scripts/wallet.js, which includes example wallet operations. <br>
Mitigation: Review, remove, or neutralize scripts/wallet.js before running npm test in any environment connected to real wallet funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kiagentkronos-cell/alby-lightning) <br>
- [Alby Hub](https://albyhub.com) <br>
- [LNURL-pay protocol](https://github.com/lnurl/luds/blob/legacy/lnurl-pay.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Text] <br>
**Output Format:** [Markdown usage guidance with bash and JSON snippets; runnable Node.js scripts return JSON payment results or terminal text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ALBY_NWC_URL and network access to recipient LNURL endpoints and the configured Alby Hub.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
