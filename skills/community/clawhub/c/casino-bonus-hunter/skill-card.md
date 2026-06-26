## Description: <br>
Ranks a static set of online casino welcome, reload, and cashback bonuses by estimated expected value and reputation score, then writes a JSON result file and console table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mibayy](https://clawhub.ai/user/Mibayy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this automaton to compare hard-coded casino bonus offers by estimated EV, wagering assumptions, and reputation-adjusted ranking. The output should be treated as decision support only, not as financial or gambling advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The ranking may be mistaken for verified live casino data or financial advice. <br>
Mitigation: Present the results as estimates from static, hard-coded data and require users to verify bonus terms, availability, legality, and personal risk before acting. <br>
Risk: The scheduled job can overwrite the path configured in BONUS_OUTPUT_FILE every six hours. <br>
Mitigation: Use a dedicated non-critical output path and avoid pointing BONUS_OUTPUT_FILE at existing user data or important system files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mibayy/casino-bonus-hunter) <br>
- [Publisher profile](https://clawhub.ai/user/Mibayy) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Files, Shell commands, Guidance] <br>
**Output Format:** [JSON file and console table] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs on a six-hour cron and writes to BONUS_OUTPUT_FILE, defaulting to /tmp/casino_bonuses.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
