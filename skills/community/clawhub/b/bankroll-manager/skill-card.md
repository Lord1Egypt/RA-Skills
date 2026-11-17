## Description:

Track bankroll across sportsbooks and prediction markets by logging bets, recording results, calculating ROI, generating P&L reports, and enforcing risk limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to track betting bankroll activity, answer P&L and ROI questions, record bet outcomes, and check stake sizes against risk limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored bankroll records may contain sensitive betting or financial information.

Mitigation: Use the skill only for bankroll tracking, avoid private details in notes, and document how users can delete or export stored records.

Risk: The shown sqlite3 command can be unsafe if populated with untrusted or unsanitized text.

Mitigation: Review commands before execution and prefer parameterized database writes for user-provided values.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rsquaredsolutions2026/skills/bankroll-manager)
- [AgentBets](https://agentbets.ai)
- [OpenClaw Bankroll Manager Skill guide](https://agentbets.ai/guides/openclaw-bankroll-manager-skill/)
- [OpenClaw Skills series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local SQLite commands and bankroll records stored at ~/.openclaw/data/bankroll.db when commands are executed.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
