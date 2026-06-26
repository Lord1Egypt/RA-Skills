## Description: <br>
Envy Trading System helps agents analyze crypto perpetual futures data, score and backtest trading signals, assemble strategies, monitor live signals, and route positions to paper or Hyperliquid executors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manolovni](https://clawhub.ai/user/manolovni) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to explore crypto market indicators, generate and score trading signals, assemble strategies, monitor live conditions, and manage paper or live perpetual futures positions with configurable risk rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can route from paper trading to live crypto perpetual futures trading, which can create real financial loss. <br>
Mitigation: Use paper mode unless live trading is explicitly intended, inspect controller.yaml before starting the controller, and confirm any switch to Hyperliquid live execution. <br>
Risk: wallet.json and config.json may contain reusable wallet or API secrets in plaintext. <br>
Mitigation: Keep the skill workspace private, do not expose wallet or config files in chat or logs, and run wallet export commands only in the user's own terminal. <br>
Risk: Security evidence marks the release suspicious because it stores wallet secrets in plaintext and can use them for live trading with limited runtime safeguards. <br>
Mitigation: Review carefully before installing, fund the generated wallet only with amounts the user can afford to lose, and validate risk rules before running the controller. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/manolovni/envy) <br>
- [OpenClaw Installation Documentation](https://docs.openclaw.ai/install) <br>
- [Envy API Discovery Endpoint](https://arena.nvprotocol.com/api/claw/discover) <br>
- [Envy API Pricing Endpoint](https://arena.nvprotocol.com/api/claw/pricing) <br>
- [Hyperliquid Application](https://app.hyperliquid.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON event examples, and YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local signal, strategy, archive, wallet, and controller configuration files when the documented commands are run.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
