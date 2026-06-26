## Description: <br>
Provides agent guidance for Moon Dev's AI trading system, including multi-agent architecture, exchange configuration, LLM provider switching, backtesting workflows, and crypto trading operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[prblmsolvrx](https://clawhub.ai/user/prblmsolvrx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-system operators use this skill to understand, configure, run, extend, and debug Moon Dev's AI trading agents across supported crypto exchanges. It also guides research and backtesting workflows that can generate executable strategy code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading guidance may result in live orders, position closures, or background trading activity. <br>
Mitigation: Use paper or testnet environments first, require manual approval before live orders or closures, and use low-balance isolated accounts for any live testing. <br>
Risk: The skill discusses private keys and exchange credentials required by trading workflows. <br>
Mitigation: Keep keys out of logs and commits, use least-privilege or no-withdrawal credentials, and review generated commands before execution. <br>
Risk: Backtesting workflows can generate and execute strategy code. <br>
Mitigation: Review generated backtest code before running it and execute it in a hardened sandbox. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/prblmsolvrx/agentqskills) <br>
- [AGENTS.md](artifact/AGENTS.md) <br>
- [WORKFLOWS.md](artifact/WORKFLOWS.md) <br>
- [ARCHITECTURE.md](artifact/ARCHITECTURE.md) <br>
- [README-claude.md](artifact/README-claude.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for running agents, editing configuration, testing exchange connections, and generating backtests.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
