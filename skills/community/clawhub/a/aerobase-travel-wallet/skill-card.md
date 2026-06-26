## Description: <br>
Credit cards, loyalty balances, transfer partners, and transfer bonuses. Calculates CPP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kurosh87](https://clawhub.ai/user/kurosh87) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and travel-rewards agents use this skill to compare credit cards, transfer partners, active transfer bonuses, loyalty wallet summaries, and cents-per-point redemption value through the Aerobase API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface wallet summaries, linked cards, transfer accounts, and loyalty balances in agent responses when an Aerobase API key is configured. <br>
Mitigation: Install only when Aerobase access is intended, keep the API key in the agent environment, avoid pasting keys into chat, and review responses before sharing them. <br>
Risk: Travel redemption guidance and CPP calculations depend on user-provided fare context and current Aerobase API data. <br>
Mitigation: Validate route, date, cabin, fare, and miles inputs before acting on recommendations, and treat results as decision support rather than a booking guarantee. <br>


## Reference(s): <br>
- [Aerobase](https://aerobase.app) <br>
- [Aerobase OpenClaw travel agent setup](https://aerobase.app/openclaw-travel-agent) <br>
- [ClawHub skill page](https://clawhub.ai/kurosh87/aerobase-travel-wallet) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Concise responses with top travel-rewards options first and one to two follow-up actions. Requires AEROBASE_API_KEY for API access.] <br>

## Skill Version(s): <br>
3.2.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
