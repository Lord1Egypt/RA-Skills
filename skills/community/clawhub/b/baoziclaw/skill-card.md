## Description: <br>
Complete Solana prediction markets skill for Baozi: list markets, get odds, place bets, and claim winnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marcusfranca12](https://clawhub.ai/user/marcusfranca12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to interact with Baozi prediction markets on Solana, including browsing markets, reviewing odds, building bet transactions, checking wallet portfolios, and preparing claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can prepare Solana betting and claim transactions and may query wallet portfolio data. <br>
Mitigation: Require explicit user confirmation before any betting or claiming action, inspect generated transaction details before signing, and avoid autonomous betting or claiming. <br>
Risk: The security evidence flags the skill as a high-impact crypto betting integration with under-scoped transaction behavior. <br>
Mitigation: Review the skill carefully before installation and use it only after trusting the external Baozi npm package and its transaction outputs. <br>
Risk: Artifact behavior includes affiliate attribution on bets. <br>
Mitigation: Make affiliate attribution visible to users before a bet is prepared or signed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marcusfranca12/baoziclaw) <br>
- [Publisher profile](https://clawhub.ai/user/marcusfranca12) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and transaction-building results from Baozi MCP tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return market, odds, portfolio, bet transaction, and claim transaction data.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
