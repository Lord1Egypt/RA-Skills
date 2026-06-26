## Description: <br>
Find, validate, and compare arbitrage opportunities across markets with fee-aware math, execution sequencing, and failure-mode checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to screen apparent price gaps, hedges, surebets, basis trades, multi-leg baskets, and cross-venue spreads. It helps produce fee-aware arbitrage analysis, execution sequencing, settlement checks, and clear rejection criteria for fake edge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local arbitrage notes could contain sensitive financial preferences, venue notes, opportunity details, account identifiers, or wallet-related information if the user records them. <br>
Mitigation: Use the scoped ~/arbitrage/ notes only for explicit preferences and opportunity notes, and keep credentials, wallet secrets, account identifiers, and sensitive financial details out of those files. <br>
Risk: Arbitrage analysis can be mistaken for trade execution guidance or a guarantee when fills, fees, settlement, venue rules, or timing assumptions are incomplete. <br>
Mitigation: Treat outputs as analysis, verify costs and settlement mechanics before acting, label soft locks and failure modes clearly, and do not execute trades or provide personalized financial, tax, or legal advice. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/arbitrage) <br>
- [Arbitrage Homepage](https://clawic.com/skills/arbitrage) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Locked Spread Protocol](artifact/workflow.md) <br>
- [Fee-Aware Arbitrage Calculator](artifact/calculator.md) <br>
- [Venue and Settlement Checks](artifact/venue-checks.md) <br>
- [Arbitrage Playbooks](artifact/playbooks.md) <br>
- [Memory Template](artifact/memory-template.md) <br>
- [Safe Language for Arbitrage Analysis](artifact/legal.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown decision memos with formulas, checklists, and occasional shell setup commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update scoped local notes under ~/arbitrage/ when the user chooses to use persistent arbitrage memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
