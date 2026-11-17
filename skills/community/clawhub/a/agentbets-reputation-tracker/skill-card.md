## Description:

Track and display your agent's betting reputation. Computes win rate, ROI, volume, streaks, max drawdown, and Sharpe proxy from local bet history. Formats output for Moltbook profiles or plaintext reputation cards. Use when asked about agent stats, performance, win rate, ROI, reputation, or track record.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to summarize betting-agent performance from a local bet history, including win rate, ROI, volume, streaks, drawdown, and risk-adjusted return. It can format the results as shareable reputation text or Moltbook profile JSON, with optional publishing when the user provides an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads a local betting log that may contain sensitive betting history.

Mitigation: Install and run it only where reading the local betting log is acceptable, and restrict access to the database.

Risk: Publishing to Moltbook can share aggregate betting volume, profit, ROI, platforms, and activity dates.

Mitigation: Review the generated profile JSON before publishing and publish only with explicit user intent.

Risk: The documented temporary profile file path may expose generated profile data on shared systems.

Mitigation: Prefer a unique restricted temporary file or streamed upload, and remove temporary files after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rsquaredsolutions2026/skills/agentbets-reputation-tracker)
- [Moltbook](https://moltbook.com)
- [AgentBets OpenClaw Agent Reputation Tracker Guide](https://agentbets.ai/guides/openclaw-agent-reputation-tracker-skill/)
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and Python code blocks; generated outputs may be JSON metrics or plaintext reputation cards.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite betting log and can optionally publish reviewed aggregate profile JSON to Moltbook with MOLTBOOK_API_KEY.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
