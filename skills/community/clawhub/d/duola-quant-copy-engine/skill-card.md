## Description: <br>
Institutional-grade execution playbook for the published `duola` Polymarket copy-trading CLI in lobster-agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duolaAmengweb3](https://clawhub.ai/user/duolaAmengweb3) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and external users use this skill to run a staged duola copy-trading workflow: verify the runtime, onboard leaders, sync and backtest strategies, run diagnostics, start limited live or autopilot operation, and report structured risk and performance results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide live Polymarket trading and persistent autopilot operation with wallet authority. <br>
Mitigation: Use a dedicated low-balance wallet, avoid exposing a main private key, require explicit approval before live trading, and monitor or stop detached autopilot promptly. <br>
Risk: The workflow depends on installing and operating the duola npm package. <br>
Mitigation: Verify the duola package and publisher independently, then pin a reviewed version before use. <br>
Risk: Billing-gated commands can create SkillPay charges. <br>
Mitigation: Require explicit approval before any billing charge and scope billing credentials to the intended user and release. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duolaAmengweb3/duola-quant-copy-engine) <br>
- [Publisher profile](https://clawhub.ai/user/duolaAmengweb3) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise structured summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented command outputs for leader, sync, backtest, doctor, and autopilot status reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
