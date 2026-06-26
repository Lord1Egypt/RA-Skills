## Description: <br>
Helps agents draft guidance, code, and commands for FinancePy-style financial date handling, curve construction, volatility modeling, and derivatives pricing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Quant developers and analysts use this skill to ask an agent for FinancePy-oriented support with business calendars, day-count conventions, schedules, yield curves, bonds, swaps, options, and pricing models. The artifacts also include ZVT market-data, backtesting, file-writing, and trading workflow guidance, so users should review generated code and commands before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Artifacts mix FinancePy pricing support with ZVT market-data, backtesting, file-writing, and trading workflows that are not clearly bounded. <br>
Mitigation: Run setup and generated commands in an isolated environment, pin and review dependencies, and require explicit confirmation before market-data collection, broker connection, or trade-related execution. <br>
Risk: Financial pricing or backtesting outputs may be misleading if inputs, date conventions, curve ordering, or execution timing assumptions are wrong. <br>
Mitigation: Validate calendars, day-count conventions, discount factors, calibration instrument order, and next-bar execution assumptions against authoritative project references before relying on results. <br>
Risk: Some workflows can write local market-data or configuration files. <br>
Mitigation: Use a dedicated writable data directory, inspect file paths before running commands, and approve file-saving behavior explicitly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tangweigang-jpg/financepy-derivatives) <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Anti-Patterns](references/ANTI_PATTERNS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference FinancePy and ZVT assumptions; generated outputs require user review before execution.] <br>

## Skill Version(s): <br>
0.3.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
