## Description:

Generates a Freqtrade short strategy for Superior Trade that enters Donchian breakdowns only when EMA separation, ADX, and recent-return gates confirm a strong bear regime.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-strategy authors use this skill to draft a regime-gated crypto futures short strategy and reference configuration for Superior Trade or Freqtrade-style workflows. The strategy should be reviewed, backtested, and paper-traded before any live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill packages high-risk trading guidance and live futures-short configuration, which can lead to significant or total loss of funds.

Mitigation: Use dry-run or paper trading first, limit API permissions and stake size, and isolate use in a sub-account.

Risk: Strong backtest framing may overstate reliability because the reported results cover a small trade sample.

Mitigation: Treat the backtest as limited evidence, run independent validation on longer and out-of-sample periods, and do not treat it as a ready-to-run profit system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/superior-ai/skills/donchian-strong-regime)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trading strategy code and reference configuration; does not execute trades by itself.]

## Skill Version(s):

1.0.0 (source: release metadata; artifact frontmatter lists 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
