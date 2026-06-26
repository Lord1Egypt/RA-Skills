## Description: <br>
Daily Stock Analyzer helps agents build and run A-share stock analysis workflows with Qlib/ZVT, LLM ReAct reasoning, technical trend screening, backtesting, portfolio diagnostics, and notification support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangweigang-jpg](https://clawhub.ai/user/tangweigang-jpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance automation users use this skill to create daily A-share analysis, screening, backtesting, portfolio review, and notification workflows. It can generate buy/hold/sell guidance, code, commands, and configuration steps for data collection and strategy execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bundles broad finance automation behavior, including trading, hosting, notification, diagnostics, persistence, and portfolio/account capabilities under a narrower daily stock-analysis description. <br>
Mitigation: Review and constrain enabled capabilities before installation; disable server, bot, diagnostics, and notification features by default unless they are deliberately needed. <br>
Risk: Finance outputs may be interpreted as actionable buy, hold, or sell advice. <br>
Mitigation: Treat all trading signals and portfolio reports as informational, require human review, and avoid broker or trading permissions unless explicitly authorized. <br>
Risk: Data credentials or stored financial data may be exposed if runtime access is broader than necessary. <br>
Mitigation: Use read-only data credentials where possible, confirm what data is persisted, and limit filesystem and secret access for the agent runtime. <br>


## Reference(s): <br>
- [Human Summary](human_summary.md) <br>
- [Known Use Cases](references/USE_CASES.md) <br>
- [Semantic Locks and Preconditions](references/LOCKS.md) <br>
- [Component Capability Map](references/COMPONENTS.md) <br>
- [Authoritative Seed](references/seed.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, configuration guidance, and generated analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include finance analysis and trading suggestions that require human review.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
