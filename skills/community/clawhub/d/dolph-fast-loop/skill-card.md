## Description: <br>
Trades Polymarket 5-minute and 15-minute crypto fast markets using CEX price momentum signals through the Simmer API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richducat](https://clawhub.ai/user/richducat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to configure, simulate, and optionally run automated Polymarket fast-market trades based on CEX crypto momentum signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute unattended real-money Polymarket trades using wallet credentials. <br>
Mitigation: Run dry-run first, use a dedicated low-balance wallet, keep live trading disabled until reviewed, and set strict per-trade and daily budget limits. <br>
Risk: Fast markets can resolve before stop-loss or take-profit monitoring can act. <br>
Mitigation: Do not rely on automated risk monitors for 5-minute or 15-minute positions; size trades for full-loss exposure and monitor live runs closely. <br>
Risk: The skill requires Simmer API access and live trading depends on private wallet key handling. <br>
Mitigation: Store credentials only in environment or secret storage, verify the Simmer SDK and publisher context, and avoid exposing keys in prompts, logs, or config files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/richducat/dolph-fast-loop) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/richducat) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and Python/configuration file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run and live-trading guidance, environment variable setup, tunable parameters, and CLI usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
