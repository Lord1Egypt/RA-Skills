## Description: <br>
Provides advanced financial machine learning guidance for information-driven bars, fractional differencing, backtesting, multi-market factor research, and strategy validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative finance practitioners use this skill to generate guidance, code, and setup steps for ZVT-based market data collection, factor research, backtesting, and strategy validation across A-share, HK, and crypto workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated financial code or backtest guidance may produce misleading strategy results if data alignment, look-ahead bias, costs, or survivorship effects are not reviewed. <br>
Mitigation: Review generated code and assumptions before execution, validate time alignment and costs, and test with out-of-sample or walk-forward methods. <br>
Risk: The skill may suggest local setup, recorder, broker, paid-provider, wallet, or credential-dependent workflows. <br>
Mitigation: Run commands in an isolated Python environment and connect broker, wallet, or provider credentials only when the user explicitly intends that workflow. <br>
Risk: The security summary notes mixed finance and documentation scopes plus automatic skill-saving behavior. <br>
Mitigation: Review requested scope carefully and decline or disable persistence behavior unless saving new skill files is desired. <br>


## Reference(s): <br>
- [Skill Overview](SKILL.md) <br>
- [Human Summary](human_summary.md) <br>
- [Semantic Locks](references/LOCKS.md) <br>
- [Constraints](references/CONSTRAINTS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Use Cases](references/USE_CASES.md) <br>
- [Wisdom](references/WISDOM.md) <br>
- [Seed YAML](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with code snippets, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local Python 3.12, uv, ZVT, data-provider, broker, or recorder workflows that should be reviewed before execution.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
