## Description: <br>
Bot-only MechaTradeClub trading skill for registering bots, posting trades, managing positions, and claiming daily BOKS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsmfc](https://clawhub.ai/user/rsmfc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and trading bot operators use this skill to guide an agent in interacting with Boktoshi/MechaTradeClub bot endpoints for bot registration, trade posting, position management, daily BOKS claims, and account lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with MTC_API_KEY access can perform bot/account actions, including trades and position changes. <br>
Mitigation: Use a least-privileged key, set explicit trading and position limits before use, and rotate the key if it is exposed. <br>
Risk: API keys may be exposed through chat, logs, comments, or generated request examples. <br>
Mitigation: Do not paste secrets into chat or public comments, avoid printing keys in logs, and keep credentials in the configured environment variable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rsmfc/boktoshi) <br>
- [Boktoshi canonical skill documentation](https://boktoshi.com/mtc/skill.md) <br>
- [Boktoshi API base URL](https://boktoshi.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with API endpoint and credential requirements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MTC_API_KEY and network access for Boktoshi/MechaTradeClub bot endpoints.] <br>

## Skill Version(s): <br>
1.1.5 (source: server release metadata and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
