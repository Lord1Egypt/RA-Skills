## Description: <br>
Finrl Meta Envs helps agents produce multi-market quantitative trading guidance, code, shell commands, and configuration for data collection, factor research, backtesting, reinforcement-learning portfolio optimization, and Alpaca paper-trading workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to generate and adapt workflows for ZVT and FinRL-style market data collection, factor engineering, backtests, Markowitz optimization, DRL agent training, and paper-trading across A-share, HK, crypto, and related markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary flags a mixed FinRL/ZVT identity and default behavior to save derived skills. <br>
Mitigation: Review generated or saved derived skills, scan them before deployment, and require explicit confirmation before persisting derived skill changes. <br>
Risk: The skill may set up Python/ZVT tooling and store market data locally. <br>
Mitigation: Run it in an isolated environment and set ZVT_HOME to a contained writable directory. <br>
Risk: The skill can generate paper-trading or broker-connected code. <br>
Mitigation: Use only paper or sandbox broker credentials unless a human explicitly authorizes live broker integration. <br>
Risk: Backtests and paper-trading outputs may be mistaken for investment advice or live-trading proof. <br>
Mitigation: Label generated trading results as simulations, require human review before financial decisions, and preserve the skill's next-bar execution and cost-model constraints. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/tangweigang-jpg/finrl-meta-envs) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Domain Constraints](references/CONSTRAINTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Cross-Project Wisdom](references/WISDOM.md) <br>
- [Seed Evidence](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, date range, and entity IDs before generating a workflow.] <br>

## Skill Version(s): <br>
0.3.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
