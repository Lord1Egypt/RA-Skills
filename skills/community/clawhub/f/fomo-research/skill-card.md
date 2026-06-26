## Description: <br>
Smart money research via Fomo social graph that helps agents track top traders, monitor live trades, and build watchlists using fomo.family data through cope.capital. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pooowell](https://clawhub.ai/user/pooowell) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to research Fomo traders, monitor public on-chain activity, build watchlists, and summarize trader behavior. It is not for executing trades, managing funds, or handling private keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Cope Capital API key. <br>
Mitigation: Keep COPE_API_KEY private, avoid exposing it in logs or messages, and revoke the key if it is compromised. <br>
Risk: Optional x402 access can trigger paid USDC-backed API calls. <br>
Mitigation: Enable x402 only after explicit user approval and review account usage regularly. <br>
Risk: Local trade logs can reveal private research interests or watchlist behavior. <br>
Mitigation: Review, protect, or delete local memory/trades logs when they are no longer needed. <br>


## Reference(s): <br>
- [Cope Capital API Reference](references/api.md) <br>
- [Interactive API docs](https://api.cope.capital/docs) <br>
- [Human docs](https://cope.capital/docs) <br>
- [Fomo](https://fomo.family) <br>
- [ClawHub skill page](https://clawhub.ai/pooowell/fomo-research) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, API request examples, and concise research summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local JSON trade logs when the user asks the agent to persist research history.] <br>

## Skill Version(s): <br>
0.3.0 (source: release evidence and CHANGELOG, released 2026-02-21) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
