## Description:

Estimate intrinsic value with a first-principles DCF from structured JSON or provider-backed ticker input, and return auditable FCFF, WACC, and per-share value output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiejiang8](https://clawhub.ai/user/tiejiang8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and research workflows use FP-DCF to produce auditable DCF valuations, market-implied growth checks, WACC and terminal-growth sensitivity outputs, and structured diagnostics from explicit fundamentals or provider-backed ticker data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes repository workflow instructions that could influence an agent to bypass normal branch or pull-request review practices.

Mitigation: Use the skill only for valuation tasks and do not grant Git publish authority while it is active.

Risk: Provider-backed runs may contact finance data providers and write local cache or output artifacts.

Mitigation: Run in a constrained environment, review generated artifacts, and refresh provider data when the user asks for current market conditions.

Risk: DCF outputs can be misleading if treated as buy, sell, portfolio, or financial-sector valuation advice.

Mitigation: Present FP-DCF as a valuation layer only, surface diagnostics and warnings, and require separate business, industry, and risk analysis before investment conclusions.

## Reference(s):

- [FP-DCF ClawHub Skill Page](https://clawhub.ai/tiejiang8/skills/fp-dcf)
- [FP-DCF Homepage](https://github.com/tiejiang8/FP-DCF)
- [FP-DCF Methodology](references/methodology.md)
- [README](README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON payload examples and shell commands; runtime execution returns structured JSON and optional sensitivity chart files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Valuation outputs may include FCFF, WACC, enterprise value, equity value, per-share value, market-implied growth, provider data freshness, diagnostics, warnings, and sensitivity artifact paths.]

## Skill Version(s):

0.5.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
