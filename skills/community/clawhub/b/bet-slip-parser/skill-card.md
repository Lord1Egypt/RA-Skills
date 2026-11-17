## Description:

Parse bet slips from text, natural language, or screenshots into structured JSON with stake, odds, bet type, selection, sportsbook, and bet-leg details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert sportsbook confirmations, natural-language bet descriptions, or bet-slip screenshots into reviewable structured JSON before logging or downstream processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bet slips can contain sensitive gambling details, including stake, odds, sportsbook, selections, and raw bet text.

Mitigation: Review the parsed JSON before storing it, sharing it, or passing it to another skill.

Risk: The skill may produce incomplete or ambiguous betting data when source text, screenshots, odds, stake, or sportsbook details are unclear.

Mitigation: Use the skill's clarification flow and keep unavailable fields as null rather than guessing.

## Reference(s):

- [ClawHub Bet Slip Parser Skill Page](https://clawhub.ai/rsquaredsolutions2026/skills/bet-slip-parser)
- [AgentBets OpenClaw Bet Slip Parser Tutorial](https://agentbets.ai/guides/openclaw-bet-slip-parser-skill/)
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills)
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON object with optional clarification prompts when critical fields are missing]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes raw input, American odds, decimal odds, implied probability, per-leg entries for parlays, nulls for unavailable fields, and calculated payout when needed.]

## Skill Version(s):

1.1.0 (source: server release metadata, created 2026-03-24T23:11:12Z)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
