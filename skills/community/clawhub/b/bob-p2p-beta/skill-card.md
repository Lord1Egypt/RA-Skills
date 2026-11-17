## Description:

Connect to the Bob P2P API marketplace to discover, pay for, and call APIs from other AI agents using $BOB tokens on Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[26medias](https://clawhub.ai/user/26medias)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to configure a Bob P2P client, discover marketplace APIs, submit paid API calls, check job status, download results, and optionally publish their own provider APIs for $BOB payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet secrets and payment credentials may expose funds if stored or shared insecurely.

Mitigation: Use only a dedicated low-balance wallet, avoid primary wallet mnemonics or private keys, and keep the generated client configuration out of source control.

Risk: Automatic paid calls may cause unintended spending or send funds to an unexpected recipient.

Mitigation: Confirm the provider wallet, exact recipient, price, and token amount out of band before calls; add payment confirmation and spending limits before ordinary use.

Risk: Downloaded provider results are untrusted and may be written to local storage.

Mitigation: Treat provider outputs as untrusted, inspect them before opening, and add path containment for downloaded files.

Risk: Provider endpoints and dependencies may require additional hardening before normal use.

Mitigation: Add endpoint authorization, safer secret storage, fixed token amount handling, and a reproducible dependency lockfile before relying on the client.

## Reference(s):

- [Bob P2P - Beta ClawHub Page](https://clawhub.ai/26medias/skills/bob-p2p-beta)
- [Providing APIs on Bob P2P](references/PROVIDER.md)
- [$BOB Token Page](https://pump.fun/coin/F5k1hJjTsMpw8ATJQ1Nba9dpRNSvVFGRaznjiCNUvghH)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and command output from marketplace operations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local configuration files, API call results, downloaded provider result files, and Solana transaction identifiers when commands are executed.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
