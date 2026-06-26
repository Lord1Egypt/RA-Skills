## Description: <br>
Provides a minimal Python client for authenticated Polymarket trading, including market and limit buy/sell orders, order lookup, and order cancellation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jvnhaowen](https://clawhub.ai/user/jvnhaowen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure and run a Python-based Polymarket trading client for authenticated order placement, order queries, and cancellations. It is intended for users who already understand Polymarket markets, wallet custody, token IDs, allowances, and trade risk. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a raw wallet private key for authenticated signing. <br>
Mitigation: Use a dedicated low-balance wallet, keep private.env out of git and synced folders, restrict file permissions, and rotate the key if exposure is suspected. <br>
Risk: The script can place market and limit orders, update allowances, and cancel orders without built-in confirmation prompts. <br>
Mitigation: Manually verify token IDs, amounts, prices, allowances, and cancellation targets before each run; avoid unattended execution. <br>
Risk: The trading client depends on external Python packages and the live Polymarket CLOB endpoint. <br>
Mitigation: Review and pin dependencies, run in an isolated environment, and confirm endpoint and network settings before using funds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jvnhaowen/autotransactions) <br>
- [Python minimal mapping](references/poly-sdk-mapping.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell commands; the included script prints JSON responses from trading actions.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local environment configuration for POLYMARKET_PRIVATE_KEY before authenticated Polymarket actions can run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
