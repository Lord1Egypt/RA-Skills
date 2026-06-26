## Description: <br>
A Share Trader helps agents run and inspect a prototype adaptive quantitative trading framework for China A-share strategy simulation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmaya](https://clawhub.ai/user/hmaya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to analyze and simulate multi-strategy China A-share trading workflows, including market-state detection, strategy weighting, risk controls, and paper or backtest-style outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading authority could be granted to a prototype that uses simulated or fallback market data. <br>
Mitigation: Run only in local simulation or paper mode, and do not provide brokerage credentials or real trading permissions until live mode is disabled or backed by a reviewed broker adapter. <br>
Risk: Buy and sell signals may be based on random or mock data and could mislead financial decisions. <br>
Mitigation: Label outputs as simulation, require verified data sources, and require explicit human confirmation before any real-money action. <br>
Risk: Performance targets and strategy outputs may be interpreted as investment advice. <br>
Mitigation: Present results as educational or analytical output only, and require independent validation and backtesting before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hmaya/a-share-trader) <br>
- [Skill Definition](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with Python code and shell commands; runtime examples may emit JSON-like trading status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Trading signals and performance examples should be treated as simulation outputs unless connected to verified real data and reviewed broker controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
