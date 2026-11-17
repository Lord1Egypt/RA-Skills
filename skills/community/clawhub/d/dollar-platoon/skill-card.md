## Description:

Peer-to-peer task payroll marketplace on Base L2 where clients create USDC-funded gigs, distribute tasks through email or webhooks, review proofs of work, and trigger on-chain payouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mevdragon](https://clawhub.ai/user/mevdragon)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to create or join Dollar Platoon gigs, submit and review proofs of work, manage Base L2 wallets and USDC payouts, and integrate task distribution through email, webhooks, or public submit links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes wallet, deposit, transfer, proof approval, and payout rollup actions with payment impact.

Mitigation: Require explicit user confirmation before deposits, transfers, proof approvals, and rollups, and verify balances, fees, recipient wallets, and gig IDs before execution.

Risk: Short URL tokens, share tokens, API keys, and install secrets may grant access to publishing or proof-submission flows if exposed.

Mitigation: Avoid using short tokens for sensitive publishing, rotate any exposed tokens or API keys, and regenerate compromised mailbox share tokens.

Risk: The security guidance flags possible misuse for fake engagement, paid reviews, account farming, or spam-related tasks.

Mitigation: Decline or escalate requests involving manipulative engagement, paid reviews, account farming, spam, illegal content, harassment, money laundering, sanctions evasion, malware, adult content, or high-risk financial services.

Risk: Inbound email and webhook payloads may include untrusted HTML or task content from third-party publisher apps.

Mitigation: Sanitize untrusted HTML before rendering or forwarding it, and review publisher app configuration and task terms before distributing work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mevdragon/skills/dollar-platoon)
- [Publisher Profile](https://clawhub.ai/user/mevdragon)
- [Skill Source Artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with REST API examples, JSON request and response bodies, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational guidance for wallet funding, proof review, payout rollups, token rotation, webhook integration, and public submit links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
