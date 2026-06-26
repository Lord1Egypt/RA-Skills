## Description: <br>
Auto-discovers Polymarket markets matching configured keywords, categories, and volume criteria, then imports matching markets into Simmer on demand or on a schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to configure market-search filters, preview matching Polymarket markets, and import selected markets into a Simmer account with quota-aware limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live scheduled imports can change the connected Simmer account and consume import quota. <br>
Mitigation: Start in dry-run mode, confirm filters and max_per_run, and enable live cron only after the expected imports and quota impact are understood. <br>
Risk: The skill requires a Simmer API key to search and import markets. <br>
Mitigation: Use a dedicated or least-privileged API key if available and install only when intentionally connecting this skill to a Simmer account. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richducat/dolph-market-importer) <br>
- [Publisher profile](https://clawhub.ai/user/richducat) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, JSON] <br>
**Output Format:** [Console text, Markdown instructions, configuration values, and optional JSON automaton status] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to dry-run behavior unless live import is explicitly enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
