## Description: <br>
Trains dynamic financial knowledge graph embedding models to learn temporal entity and relation representations for link prediction and event time prediction. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and financial researchers use this skill to build dynamic financial knowledge graph embedding workflows and related ZVT research/backtesting code for A-share, HK, or crypto market analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release combines knowledge graph model training with ZVT quant/backtesting and broker/provider workflow guidance. <br>
Mitigation: Use it only for research or paper/backtest workflows unless the skill is updated to clearly declare credential scope and require explicit confirmation for any broker-connected action. <br>
Risk: Generated financial workflows may depend on local ZVT setup and persistent market data directories. <br>
Mitigation: Run setup in an isolated Python environment and set ZVT_HOME to a controlled directory before executing generated commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tangweigang-jpg/finance-kg-embedding) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks](references/LOCKS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with code snippets and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for target market, data provider, strategy type, date range, and entity IDs before generating workflow guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
