## Description: <br>
Generates a concise daily cryptocurrency market brief from current search results, including BTC/ETH market snapshots, major events, funding-rate context, and optional Feishu delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcy891](https://clawhub.ai/user/pcy891) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Crypto-focused users and analysts use this skill to request a daily market briefing that summarizes BTC/ETH conditions, recent cryptocurrency events, funding-rate observations, and concise action-oriented notes. The skill is not a source of investment advice and should rely on retrieved data rather than invented prices or rates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send generated briefing content to a fixed Feishu recipient without clear per-request user control. <br>
Mitigation: Install only when the Feishu destination is understood and controlled; confirm or remove the hardcoded open_id and require confirmation before sending messages. <br>
Risk: The briefing depends on current cryptocurrency search results and may become misleading if retrieved prices, funding rates, or events are stale or absent. <br>
Mitigation: Verify current-market inputs before acting on the output, preserve the skill behavior of saying data is unavailable when evidence is missing, and treat the briefing as informational rather than investment advice. <br>
Risk: The artifact references miaoda-studio-cli for searches, which may introduce tool behavior outside the skill text. <br>
Mitigation: Verify the referenced CLI and its data sources before allowing the skill to run searches in an agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcy891/crypto-daily-briefing) <br>
- [Source skill artifact](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with tables, bullets, and inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use up to three current-market searches and may send the generated briefing to a configured Feishu destination.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
