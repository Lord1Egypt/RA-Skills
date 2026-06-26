## Description: <br>
Find markets where Simmer's AI consensus diverges from the real market price, then trade on the mispriced side using calibration-shrunk Kelly sizing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boeingchoco](https://clawhub.ai/user/boeingchoco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to scan Simmer and Polymarket market data for AI-versus-market price divergence, review filtered opportunities, and optionally execute live trades with configured Kelly sizing and budget controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real-money trades when run in live mode. <br>
Mitigation: Start in scan-only, managed, or paper trading mode, then use small budget and per-trade limits before enabling live execution. <br>
Risk: A wallet private key can control funds when external-wallet self-custody trading is used. <br>
Mitigation: Do not provide a private key unless required for the chosen trading mode, and use a wallet with limited funds. <br>
Risk: The security summary notes an automatic portfolio action that may redeem winning positions at startup. <br>
Mitigation: Review startup behavior and portfolio actions before granting credentials or running the skill against a funded account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/boeingchoco/boeingchoco-polymarket-ai-divergence) <br>
- [Publisher Profile](https://clawhub.ai/user/boeingchoco) <br>
- [Simmer API](https://api.simmer.markets) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance, terminal output, and optional JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute live trades when run with live mode and valid credentials; defaults include scan-only commands and configurable risk controls.] <br>

## Skill Version(s): <br>
2.6.1 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
