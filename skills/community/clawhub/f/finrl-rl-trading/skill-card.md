## Description: <br>
Supports FinRL-style reinforcement learning trading workflows for market data acquisition, model training, backtesting, paper trading, and performance review. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative researchers use this skill to generate guidance, code, commands, and configuration for reinforcement learning trading experiments, including data preparation, agent training, backtesting, and paper-trading workflows. Use should remain controlled because the server security review flags identity conflicts and unclear safeguards around broker/API-backed trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security review flags conflicting FinRL and ZVT skill identity signals, which can make generated trading workflow guidance unreliable. <br>
Mitigation: Confirm the intended framework and data model before using generated output, and review any produced code against the selected framework's documentation. <br>
Risk: The skill discusses broker or API-backed trading without clear safeguards for live execution, credentials, confirmations, and trading limits. <br>
Mitigation: Use an isolated research environment, avoid live broker credentials, prefer paper trading or backtesting, and require explicit human confirmation before any order-capable workflow. <br>
Risk: Dependency and execution requirements are not fully pinned in the evidence. <br>
Mitigation: Pin dependencies in a disposable Python environment and inspect generated commands or code before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/finrl-rl-trading) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/tangweigang-jpg) <br>
- [Known use cases](references/USE_CASES.md) <br>
- [Semantic locks](references/LOCKS.md) <br>
- [Domain constraints](references/CONSTRAINTS.md) <br>
- [Component capability map](references/COMPONENTS.md) <br>
- [Anti-patterns](references/ANTI_PATTERNS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request market, data source, strategy type, time range, and target entity identifiers before producing trading workflow guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
