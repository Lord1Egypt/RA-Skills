## Description:

Guides an agent to analyze stock trading opportunities, market structure, trading psychology, strategy, and risk control using Chan Theory and CZSC concepts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenghd511](https://clawhub.ai/user/chenghd511)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to structure Chan Theory stock and market analysis, including buy/sell point review, market trend assessment, trading strategy drafting, and risk-control guidance. The included scripts can fetch market data, inspect CZSC structures, and generate signal-oriented console analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Actionable stock-trading guidance may be incorrect or misleading.

Mitigation: Use the skill as educational market-analysis support only and independently verify outputs before making any trading decision.

Risk: A real Tushare token can be exposed if passed directly on the command line.

Mitigation: Use safer secret handling when running scripts and avoid placing real tokens in shell history or shared logs.

Risk: Script behavior depends on unpinned Python packages.

Mitigation: Run scripts in an isolated environment and pin and verify dependencies before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chenghd511/skills/czsc)
- [Chan Theory Core](references/chan-theory-core.md)
- [Usage Scenarios](examples/usage-scenarios.md)
- [CZSC Script Guide](scripts/README.md)
- [waditu/czsc](https://github.com/waditu/czsc)
- [Tushare](https://tushare.pro/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell examples, plus console text from optional scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script examples use CSV market data and may call Tushare with a user-provided token.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
