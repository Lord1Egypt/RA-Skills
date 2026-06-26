## Description: <br>
Run and iterate a self-hosted ClawSwap AI trading agent with Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawperp](https://clawhub.ai/user/clawperp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-agent operators use this skill to run a self-hosted ClawSwap agent, backtest strategies, download market data, and test strategy behavior before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can submit trading actions through a self-hosted trading client. <br>
Mitigation: Start in paper mode and verify the connected agent cannot affect real funds before running strategies. <br>
Risk: The skill stores credentials and runtime tokens locally. <br>
Mitigation: Protect or delete .runtime_token and .clawswap_api_key when they are no longer needed, and avoid passing API keys on the command line. <br>
Risk: Custom strategy files can run Python code without strong safety boundaries. <br>
Mitigation: Run only strategy files you fully trust and review custom strategy code before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawperp/clawswap) <br>
- [ClawSwap homepage](https://clawswap.trade) <br>
- [ClawSwap settings](https://clawswap.trade/settings) <br>
- [ClawSwap Discord](https://discord.gg/clawswap) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python command examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing instructions for running strategy loops, backtests, market-data downloads, and credential configuration.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
