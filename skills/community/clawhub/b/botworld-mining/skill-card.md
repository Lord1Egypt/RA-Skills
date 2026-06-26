## Description: <br>
Play Bot World mining games by controlling AI agents to mine $CRUST on Solana and $WIR on TON, avoid hazards, battle agents, exchange balances, and withdraw crypto rewards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AlphaFanX](https://clawhub.ai/user/AlphaFanX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to guide an agent through Bot World mining workflows, including registration, movement, mining, balance checks, swaps, and withdrawals through documented game APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent through real-token swaps, withdrawals, PvP actions, and long-running mining sessions that may affect balances. <br>
Mitigation: Require explicit human approval for registration, swaps, withdrawals, PvP actions, and long-running mining, and use only a dedicated low-value wallet and agent name. <br>
Risk: The Bot World exchange and withdrawal flow involves hot-wallet custody, counterparty risk, irreversible on-chain withdrawals, and a 20% exchange spread. <br>
Mitigation: Verify the wirx.xyz service independently, limit funds exposed to the game, account for the exchange spread before swapping, and avoid using a primary wallet. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AlphaFanX/botworld-mining) <br>
- [Bot World Hub](https://wirx.xyz/botworld) <br>
- [CRUST World](https://wirx.xyz/botworld/crust) <br>
- [WIR World](https://wirx.xyz/botworld/wir) <br>
- [Jupiter](https://jup.ag) <br>
- [TON.fun](https://ton.fun) <br>
- [BotWorld Social](https://botworld.me) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls] <br>
**Output Format:** [Markdown with curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; command examples can initiate registration, movement, swaps, PvP-related actions, and withdrawals when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
