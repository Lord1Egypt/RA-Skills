## Description: <br>
AI Model Team - Multi-model prediction system (Kronos + Chronos-2 + TimesFM + VADER) for OKX crypto and US stocks. Features error handling, retry logic, HTTP caching, unit tests, and correct data source routing (OKX for crypto, Yahoo Finance for stocks). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[erongcao](https://clawhub.ai/user/erongcao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate multi-model trading prediction signals for OKX crypto instruments and US stocks. It supports command-line analysis, concise signal output, and JSON output for downstream workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes external code imports, local package patching, and rollback-style helpers that can mutate the runtime environment. <br>
Mitigation: Install in an isolated environment, review scripts before execution, and run post_install.py or rollback helpers only when those local changes are intended. <br>
Risk: Environment-controlled paths and webhook settings can cause data to be read from or sent to untrusted locations. <br>
Mitigation: Avoid untrusted values for AI_HEDGE_PATH, ALERT_WEBHOOK, and related path settings; keep secrets out of logs and configuration files. <br>
Risk: run_team.py can write prediction notes into a local Obsidian vault instead of behaving as a read-only forecast. <br>
Mitigation: Set the vault path deliberately, run the skill in a sandbox when evaluating it, and review generated notes before relying on them. <br>
Risk: Trading predictions may be incorrect or misleading and are not investment advice. <br>
Mitigation: Treat outputs as informational signals, require human review, and apply independent risk controls before any trading decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/erongcao/ai-model-team) <br>
- [Kronos-Base Model Card](docs/KRONOS_MODEL_CARD.md) <br>
- [TimesFM dependency source](https://github.com/google-research/timesfm.git@f085b90) <br>
- [Chronos forecasting dependency source](https://github.com/amazon-science/chronos-forecasting.git@6d68ed7c4ed2805d122d77b4660765b4089de5ca) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Console text, optional JSON, and Markdown notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call external market and news APIs; run_team.py can write local notes when configured.] <br>

## Skill Version(s): <br>
2.9.2 (source: server release evidence and README.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
