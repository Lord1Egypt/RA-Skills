## Description: <br>
Smart Agent Skill scans Polymarket prediction markets for a configurable thesis, compares a user-supplied fair probability to market prices, and proposes or executes trades when the edge clears a configured threshold. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gulangduchuangtianyu](https://clawhub.ai/user/gulangduchuangtianyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to scan Polymarket markets, compare a thesis probability with current market prices, and produce dry-run trade decisions or live trades when explicitly enabled. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live mode can place real-money Polymarket trades on a recurring 15-minute schedule. <br>
Mitigation: Keep RUN_LIVE unset unless live trading is intentional, keep trade sizes small, and monitor scheduled runs. <br>
Risk: The skill requires an AION_API_KEY for market reads and trade execution. <br>
Mitigation: Use a limited or test key when available, store it as a secret, and rotate it if exposed. <br>
Risk: A stale or incorrect thesis probability can produce misleading trade decisions. <br>
Mitigation: Review dry-run decisions, market context, warnings, and edge thresholds before enabling live trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gulangduchuangtianyu/ai-skill-trader) <br>


## Skill Output: <br>
**Output Type(s):** [Text, API calls, Guidance] <br>
**Output Format:** [Terminal text summary with risk alerts, market decisions, and order updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live mode can place trades when enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
