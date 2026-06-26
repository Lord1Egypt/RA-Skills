## Description: <br>
AI Economic Tracker helps agents track balances, income, costs, runway, service-value estimates, and work-or-learn decisions from local JSONL records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor an AI agent's local economic state, record income and costs, estimate service value, and choose whether to prioritize earning work or learning based on runway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction descriptions and balances may contain sensitive financial or operational context in local records. <br>
Mitigation: Store the tracker data directory in an access-controlled location and avoid entering secrets or unnecessary personal data in descriptions. <br>
Risk: Optional cron usage can create recurring reports or writes without interactive review. <br>
Mitigation: Add the cron entry only when scheduled daily tracking is intended, and review or remove it when the skill is no longer in use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/ai-economic-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/dagangtj) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [CLI text, JSON status objects, Markdown-style reports, and command/configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes append-only local JSONL records for balances, costs, and income.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
