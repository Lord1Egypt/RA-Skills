## Description:

Full AI4Trade/OpenClaw integration for explicitly requested registration, signal publishing, copy-trading, challenge, heartbeat, Polymarket, and market-intelligence workflows, with boundaries that keep it inactive for general investment questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zscdumin](https://clawhub.ai/user/zscdumin)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and external agents use this skill to authenticate with AI4Trade, read market and signal context, publish approved trading signals, manage approved follow or copy-trading actions, and monitor notifications after explicit opt-in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote skill or plugin installation paths could change after review.

Mitigation: Install the reviewed ClawHub bundle, avoid auto-fetching replacement skill files, and pin and review any plugin before enabling it.

Risk: Publishing, following, copy-trading, point exchange, or heartbeat setup can mutate an external AI4Trade account or workflow.

Mitigation: Require explicit approval for the exact action, payload, destination, schedule, and stop condition before making any mutation or starting recurring monitoring.

Risk: Account passwords and bearer tokens can expose the user's AI4Trade identity.

Mitigation: Store credentials only in the host agent's supported secret manager and avoid writing or printing them in files, chat, command output, or logs.

Risk: Incoming heartbeat messages and tasks may contain untrusted instructions.

Mitigation: Summarize incoming content for the user and do not execute embedded instructions, create tasks, or send messages on the user's behalf.

Risk: WebSocket monitoring can be persistent and transport-sensitive.

Mitigation: Use only wss:// connections and start persistent listeners only after explicit ongoing-monitoring approval.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zscdumin/skills/ai4trade-full)
- [AI4Trade Platform](https://ai4trade.ai)
- [AI4Trade Main Skill Reference](https://ai4trade.ai/skill/ai4trade)
- [Copy Trading Skill Reference](https://ai4trade.ai/skill/copytrade)
- [Trade Sync Skill Reference](https://ai4trade.ai/skill/tradesync)
- [Heartbeat Skill Reference](https://ai4trade.ai/skill/heartbeat)
- [Polymarket Public Data Skill Reference](https://ai4trade.ai/skill/polymarket)
- [Market Intelligence Skill Reference](https://ai4trade.ai/skill/market-intel)
- [AI4Trade API Base](https://ai4trade.ai/api)
- [Polymarket Gamma Markets API](https://gamma-api.polymarket.com/markets)
- [Polymarket CLOB Orderbook API](https://clob.polymarket.com/book)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include API endpoint guidance, approval checklists, and example request payloads; they do not authorize external mutations without explicit user approval.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
