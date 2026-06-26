## Description: <br>
Use Futu Trade Bot Skills to run account, quote, and trade workflows with real HK market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeffersonling1217-png](https://clawhub.ai/user/jeffersonling1217-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agent users and developers use this skill to configure Futu OpenD access, inspect accounts and HK market quotes, place or manage Futu orders, and run simple trading strategy scripts from natural-language requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can unlock Futu accounts and place, modify, or cancel real-money orders. <br>
Mitigation: Keep SIMULATE as the default trading environment and require explicit human approval before unlocking REAL trading or submitting, modifying, or canceling orders. <br>
Risk: The skill can cancel all orders and run background strategy processes. <br>
Mitigation: Confirm account, environment, symbol, quantity, and order scope before calling cancel_all_orders or launching long-running strategy scripts; record PID and log paths for monitoring and stop actions. <br>
Risk: Configuration and generated account cache files may contain sensitive trading credentials or account data. <br>
Mitigation: Avoid plaintext trade passwords, prefer protected credential handling, keep config and account_info.json out of shared storage, and restrict file permissions for local configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jeffersonling1217-png/futu-trading-bot) <br>
- [README](README.md) <br>
- [Account Manager documentation](docs/account.md) <br>
- [Config Manager documentation](docs/config.md) <br>
- [Quote Service documentation](docs/quote.md) <br>
- [Trade Service documentation](docs/trade.md) <br>
- [Strategy Helpers documentation](docs/strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python snippets, shell commands, JSON configuration, and function call patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Python strategy scripts, process commands, account or quote summaries, order-management guidance, and local configuration instructions.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
