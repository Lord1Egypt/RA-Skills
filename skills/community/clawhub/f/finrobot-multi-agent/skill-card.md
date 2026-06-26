## Description: <br>
Finrobot Multi Agent helps agents build financial analysis and quantitative trading workflows, including equity research reports, market forecasting, filing analysis, and backtesting over global market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Financial analysts, investors, and quantitative developers use this skill to plan and generate financial data collection, research-report, RAG analysis, strategy coding, and backtesting workflows. It is especially oriented toward A-share, HK, and crypto workflows with explicit safeguards for time-series trading logic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive financial credentials may be required for data-provider or broker-connected workflows. <br>
Mitigation: Use read-only financial API keys where possible and avoid broker or trading credentials unless explicitly needed. <br>
Risk: Persistent generated outputs, vector stores, ZVT data, and memory-derived context may not be clearly scoped. <br>
Mitigation: Confirm where generated skills, vector stores, ZVT data, and memory-derived context are stored and how they can be cleared before use. <br>
Risk: Generated financial analysis or trading code can be misleading if source files and trading constraints are not reviewed. <br>
Mitigation: Review the full seed and reference files before installation or execution, and enforce the documented no-look-ahead, next-bar execution, and market-rule constraints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/finrobot-multi-agent) <br>
- [Human summary](human_summary.md) <br>
- [Known use cases](references/USE_CASES.md) <br>
- [Semantic locks and preconditions](references/LOCKS.md) <br>
- [Component capability map](references/COMPONENTS.md) <br>
- [Anti-patterns](references/ANTI_PATTERNS.md) <br>
- [Cross-project wisdom](references/WISDOM.md) <br>
- [Authoritative seed](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May depend on user-provided market, data provider, strategy type, date range, target entities, and API credentials.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
