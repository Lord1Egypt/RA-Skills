## Description: <br>
Execute BNB Chain EVM swing trades after importing a private key: buy when trigger price exceeds market condition, then place 5% take-profit and 3% stop-loss management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happyRstudent](https://clawhub.ai/user/happyRstudent) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and traders can use this skill to configure and run a BNB Chain band-trading bot with fixed entry, take-profit, and stop-loss rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to provide a raw wallet private key, which can expose funds if used with a main wallet or unsafe environment. <br>
Mitigation: Run dry-run mode first and use only a dedicated low-balance wallet for experimentation; never use a main wallet private key. <br>
Risk: The included quote, swap, gas, balance, slippage, and transaction-failure handling are placeholders rather than production trading controls. <br>
Mitigation: Do not use real funds until those components are independently implemented, audited, and tested for the intended exchange path. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown with inline bash commands and Python script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires environment variables for wallet key, RPC URL, token pair, trigger price, position size, take-profit, stop-loss, and polling interval.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
