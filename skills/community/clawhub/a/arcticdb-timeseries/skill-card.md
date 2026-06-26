## Description: <br>
Helps manage large-scale time-series data storage and querying with ArcticDB, including DataFrame lazy loading, batch concatenation, aggregation at billion-row scale, and AWS S3-compatible storage backends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data engineers use this skill to plan and generate ArcticDB-oriented workflows for high-volume time-series storage, query, versioning, and DataFrame handling. The artifact also includes quant strategy and backtesting guidance for A-share, HK, and crypto workflows, so users should review scope before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill scope expands beyond ArcticDB storage help into ZVT quant strategy, backtesting, broker-related inputs, and automatic skill-writing behavior. <br>
Mitigation: Install only when that broader ZVT and financial backtesting scope is intended, and review generated code or skill changes before applying them. <br>
Risk: The skill may involve sensitive financial data credentials or broker-connected workflows. <br>
Mitigation: Use least-privilege, preferably read-only credentials; keep secrets out of source files; and require explicit human approval before any broker-connected or account-affecting action. <br>
Risk: Generated workflows may depend on external market data services with rate limits and provider-specific behavior. <br>
Mitigation: Run in an isolated virtual environment with pinned dependencies, configure provider-specific throttling, and validate outputs against the selected data source before relying on results. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tangweigang-jpg/arcticdb-timeseries) <br>
- [Publisher Profile](https://clawhub.ai/user/tangweigang-jpg) <br>
- [Use Cases](artifact/references/USE_CASES.md) <br>
- [Constraints](artifact/references/CONSTRAINTS.md) <br>
- [Semantic Locks](artifact/references/LOCKS.md) <br>
- [Anti-Patterns](artifact/references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](artifact/references/COMPONENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask for market, data provider, strategy type, time range, and target entity IDs before producing implementation guidance.] <br>

## Skill Version(s): <br>
0.3.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
