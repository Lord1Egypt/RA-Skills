## Description: <br>
Runs a complete local Dawn strategy workflow: authenticate, research markets with SDK tools, generate Python strategy code, launch background runs, monitor logs, and stop strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[njdawn](https://clawhub.ai/user/njdawn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill to set up Dawn CLI, research prediction markets, create local Python strategies, and manage paper or live strategy runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live wallet trading and background strategies can place real-money trades or access portfolio data. <br>
Mitigation: Start in paper mode, use small budgets, and require explicit confirmation before any live launch, sell, redeem, or LLM-agent strategy that can trade or view portfolio data. <br>
Risk: Sensitive credentials and wallet access are required for authenticated or live workflows. <br>
Mitigation: Protect DAWN_JWT_TOKEN, API keys, and wallet access; avoid exposing them in logs, strategy code, or shared environments. <br>
Risk: Generated or downloaded Python strategies and dependencies may behave unexpectedly. <br>
Mitigation: Review strategy code and dependencies before launch, monitor logs after startup, and stop runs that deviate from the intended behavior. <br>


## Reference(s): <br>
- [Dawn homepage](https://dawn.ai) <br>
- [Dawn dashboard](https://cli.dawn.ai/dashboard) <br>
- [Dawn API](https://api.dawn.ai) <br>
- [OpenWallet](https://openwallet.sh/) <br>
- [LiteLLM provider documentation](https://docs.litellm.ai/docs/providers) <br>
- [ClawHub skill page](https://clawhub.ai/njdawn/dawn-cli) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/njdawn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local strategy files and Dawn CLI commands; live trading actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.4.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
