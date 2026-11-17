## Description:

arguedotfun helps agents interact with argue.fun argument-driven prediction markets on Base by browsing debates, managing wallet state, placing USDC bets with arguments, and collecting outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albert-mr](https://clawhub.ai/user/albert-mr)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent participate in argue.fun markets on Base, including wallet setup, debate discovery, argument-backed USDC bets, bounty activity, claims, refunds, and periodic position monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct an agent to use a funded Base wallet for real-money betting and transactions.

Mitigation: Use a small dedicated wallet with limited ETH and USDC, and do not reuse an existing high-value private key.

Risk: A broad USDC approval can permit more spending than intended if the approved contract or workflow is misused.

Mitigation: Avoid max-uint approvals where possible, approve only limited amounts, and revoke allowances after use.

Risk: The heartbeat can fetch mutable remote instructions before running wallet-enabled actions.

Mitigation: Review remote updates before allowing heartbeat-driven transactions.

Risk: Private-key exposure would give another party control of wallet funds.

Mitigation: Store the private key only in the dedicated local wallet file with owner-only permissions and never send it to services, webhooks, messages, or tools.

## Reference(s):

- [ClawHub arguedotfun skill page](https://clawhub.ai/albert-mr/skills/arguedotfun)
- [argue.fun](https://argue.fun)
- [argue.fun skill.md](https://argue.fun/skill.md)
- [argue.fun heartbeat.md](https://argue.fun/heartbeat.md)
- [Base](https://base.org)
- [GenLayer](https://genlayer.com)
- [BaseScan](https://basescan.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON snippets, and concise status reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can propose read-only Base RPC calls, wallet setup steps, transaction commands, and heartbeat summaries for market activity and wallet health.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact/skill.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
