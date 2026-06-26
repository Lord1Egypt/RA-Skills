## Description: <br>
Parses bet slips from text, natural language, or screenshots into structured JSON with stake, odds, bet type, selection, and sportsbook fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsquaredsolutions2026](https://clawhub.ai/user/rsquaredsolutions2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert betting slip text, natural-language betting descriptions, or screenshots into reviewable structured JSON for logging and follow-up workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bet slips or screenshots can contain account numbers, balances, personal identifiers, or unrelated sensitive content. <br>
Mitigation: Redact sensitive details before sharing inputs, and review the parsed JSON before using it for records. <br>
Risk: Parsed betting details may be incomplete or inaccurate when the source text is ambiguous, cropped, blurry, or missing stake, odds, or sportsbook information. <br>
Mitigation: Ask for missing critical fields, use null rather than guesses for unavailable values, and verify the result against the original slip before relying on it. <br>


## Reference(s): <br>
- [Bet Slip Parser on ClawHub](https://clawhub.ai/rsquaredsolutions2026/bet-slip-parser) <br>
- [AgentBets Bet Slip Parser Tutorial](https://agentbets.ai/guides/openclaw-bet-slip-parser-skill/) <br>
- [OpenClaw Skills Series](https://agentbets.ai/guides/#openclaw-skills) <br>
- [Agent Betting Stack](https://agentbets.ai/guides/agent-betting-stack/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Guidance, Shell commands] <br>
**Output Format:** [JSON object with optional clarification prompts and inline shell commands for validation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires vision-capable models for screenshots; asks for missing critical fields and asks the user to confirm parsed JSON.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
