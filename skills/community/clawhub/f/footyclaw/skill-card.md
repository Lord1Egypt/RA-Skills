## Description: <br>
FootyClaw helps agents analyze football betting opportunities by fetching odds, calculating expected value and Kelly stake sizing, checking fundamentals, recommending bet plans, and maintaining a conversation-based ledger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[botaocai](https://clawhub.ai/user/botaocai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to scan football odds, evaluate positive-EV betting candidates, size stakes against a bankroll, and format betting and ledger summaries. Outputs should be treated as informational analysis and independently verified before any betting decision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses The Odds API and may consume API quota while scanning football odds. <br>
Mitigation: Configure ODDS_API_KEY through the skill settings or environment only, monitor quota, and avoid sharing or printing the key in conversation. <br>
Risk: Betting recommendations, EV calculations, and Kelly stake sizing can be wrong, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as informational analysis, independently verify odds and assumptions, and do not rely on the skill as financial advice. <br>
Risk: Bankroll, stakeholder, and betting ledger details may remain in the agent conversation context. <br>
Mitigation: Share only ledger and bankroll information appropriate for the agent context and clear or limit retained context according to the user's privacy needs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/botaocai/footyclaw) <br>
- [Betting rules reference](references/betting-rules.md) <br>
- [Fundamental analysis framework](references/fundamental-analysis.md) <br>
- [The Odds API](https://the-odds-api.com) <br>
- [The Odds API v4 endpoint](https://api.the-odds-api.com/v4) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown betting analysis with inline shell commands and optional Base64 SVG image output from helper scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ODDS_API_KEY from the environment for odds API calls; betting ledger data is maintained in agent conversation context.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
