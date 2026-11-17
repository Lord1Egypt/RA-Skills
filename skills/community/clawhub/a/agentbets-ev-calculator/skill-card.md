## Description:

Calculate expected value for sports bets or prediction market positions using American odds, decimal odds, implied probability, Kalshi contract prices, and an estimated true probability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to evaluate whether a sports bet or prediction market position is positive or negative EV, compare lines, and calculate breakeven probability from supported odds formats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Instructions place user-provided values into a shell command in a potentially unsafe way.

Mitigation: Review before installing; validate numeric inputs and invoke Python with structured arguments, or perform the calculation directly without a shell command.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rsquaredsolutions2026/skills/agentbets-ev-calculator)
- [AgentBets EV Calculator Guide](https://agentbets.ai/guides/openclaw-ev-calculator-skill/)
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline bash code blocks and calculated EV summary text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; calculations depend on user-provided odds and true-probability inputs.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
