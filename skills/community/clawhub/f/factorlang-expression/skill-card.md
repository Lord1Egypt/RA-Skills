## Description:

Provides a FactorLang quantitative factor expression reference for writing factor expressions, querying syntax, and designing trading strategy conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rxjhfmf](https://clawhub.ai/user/rxjhfmf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative strategy authors use this skill to look up FactorLang syntax, variables, functions, and examples when drafting factor expressions and trading strategy conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated trading rules may be incorrect, misleading, or unsuitable for a user's financial context.

Mitigation: Review generated rules carefully and treat examples as technical templates rather than financial recommendations.

Risk: Backtest or execution-related tool calls could run with unintended strategy parameters.

Mitigation: Require explicit user confirmation before any MCP, backtest, or execution-related tool use.

## Reference(s):

- [FactorLang expression system specification](artifact/resources/FactorLang表达式系统规范.md)
- [ClawHub skill page](https://clawhub.ai/rxjhfmf/skills/factorlang-expression)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with FactorLang expression snippets and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include strategy-expression examples and user-directed MCP/backtest call parameters; examples should not be treated as financial recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
