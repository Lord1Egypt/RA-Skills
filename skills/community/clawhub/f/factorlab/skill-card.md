## Description:

Factorlab analyzes A-share stocks with a three-factor quantitative model and produces stock scores, buy/hold/avoid style signals, supporting reasons, and risk notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hunkguo](https://clawhub.ai/user/hunkguo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to analyze individual A-share stocks or scan a stock pool for multi-factor scores, recommendations, reasons, and risk prompts. It is intended for quantitative research support, not personalized investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce explicit buy-oriented recommendation labels that may be mistaken for personal financial advice.

Mitigation: Treat outputs as research signals, preserve the non-investment-advice warning, and require human financial judgment before acting.

Risk: Live mode may contact configured TDX market data servers and may fall back to simulated data when live data is unavailable.

Mitigation: Run in a virtual environment, pin optional dependencies such as pytdx, check the reported data-source label, and use --no-live when network access is not intended.

## Reference(s):

- [Factor theory reference](references/factor_theory.md)
- [ClawHub skill page](https://clawhub.ai/hunkguo/skills/factorlab)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown reports by default, or JSON when requested with the CLI flag]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes factor scores, recommendation labels, confidence, reasons, risk prompts, and data-source labeling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
