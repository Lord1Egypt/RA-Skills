## Description: <br>
Crypto Trading Agents helps agents analyze cryptocurrency markets, generate trading signals, and prepare Binance spot-trading actions through a multi-agent workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kriouerlia](https://clawhub.ai/user/kriouerlia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-system builders use this skill to connect multi-agent crypto analysis with Binance spot-market workflows, including account status checks, signal generation, and optional order execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate real Binance trades and expose trading or account details through external notification channels. <br>
Mitigation: Use Binance testnet first, keep auto-trading disabled until reviewed, and avoid notification integrations unless the data-sharing impact is understood. <br>
Risk: Credential misuse could lead to unauthorized trading or broader account impact. <br>
Mitigation: Restrict API keys to the minimum required permissions, disable withdrawals, store secrets outside source control, and rotate keys if exposure is suspected. <br>
Risk: Setup steps pull and install external code and tooling before use. <br>
Mitigation: Inspect and pin the external repository and dependencies, avoid curl-to-shell installation, and review generated commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kriouerlia/crypto-trading-agents) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include trading-analysis instructions, environment-variable setup, and command examples for Binance and notification workflows.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
