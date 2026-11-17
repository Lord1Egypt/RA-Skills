## Description:

DanceTech Protocol (DanceArc) helps agents work with Arc Testnet native USDC, HTTP 402 x402-shaped challenges, Circle Gateway verification, and h2h/h2a/a2a/a2h settlement patterns.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use DanceArc to implement, explain, or debug Arc Testnet USDC pay-per-call APIs, x402-style 402 challenge flows, Circle Gateway verification, and human/agent payment workflows for battle, coaching, beats, and judge-score scenarios.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet actions and payment calls can transfer funds to the wrong recipient or on the wrong chain if challenge details are not checked.

Mitigation: Use Arc Testnet only, confirm payment amounts and recipients before signing, and verify chain, recipient, and per-action pricing with GET /api/health.

Risk: Circle credentials, entity secrets, private keys, or .env values could be exposed through browser-side code, logs, or agent prompts.

Mitigation: Keep secrets server-side or local, do not commit .env files, and prevent agents from echoing ARC_BURST_PRIVATE_KEY or Circle credentials into browser context.

Risk: Payment verification can fail or race if receipts are not yet indexed, recipients are invalid, or submitted transaction hashes do not match the challenge.

Mitigation: Wait for transaction receipts, validate recipient, value, sender, and chain against the challenge, and inspect ArcScan before retrying paid requests.

## Reference(s):

- [DanceArc ClawHub listing](https://clawhub.ai/arunnadarasa/skills/dancearc)
- [DanceArc repository](https://github.com/arunnadarasa/dancearc)
- [DanceArc API routes](artifact/references/api-routes.md)
- [x402-style payment flow](artifact/references/payment-flow.md)
- [OpenClaw workspace hints](artifact/references/openclaw-workspace.md)
- [Arc docs - Connect to Arc](https://docs.arc.network/arc/references/connect-to-arc)
- [Circle Modular Wallets Web SDK](https://developers.circle.com/w3s/modular-wallets-web-sdk)
- [Circle Nanopayments](https://developers.circle.com/gateway/nanopayments)
- [x402 package](https://www.npmjs.com/package/x402)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, API routes, environment-variable tables, and troubleshooting steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; may guide Arc Testnet payment calls, wallet confirmation steps, and secret-handling precautions.]

## Skill Version(s):

0.1.0 (source: server release evidence and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
