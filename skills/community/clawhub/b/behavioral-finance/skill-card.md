## Description:

Identifies behavioral finance patterns, market sentiment extremes, herding, anchoring, and contrarian trading signals for stock analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmaya](https://clawhub.ai/user/hmaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to run JSON-driven behavioral finance analysis that detects cognitive-bias patterns, quantifies sentiment, and produces contrarian signals and risk warnings for stock lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulated or random trading analysis may be mistaken for actionable investment guidance.

Mitigation: Treat outputs as demonstration-only financial logic unless the publisher adds real data-provider integration, deterministic calculations, reproducible backtests, and clear synthetic-data warnings.

Risk: Automated trading use could act on unsupported recommendations.

Mitigation: Do not connect this skill to automated trading or rely on its recommendations for real investment decisions in its current form.

Risk: Financial outputs lack server-resolved provenance for the underlying source version.

Mitigation: Review the artifact and publisher context carefully before installation or deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON response with behavioral analysis, trading signal, backtest, sentiment, and risk warning fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts JSON parameters via command line or stdin; requires Python packages listed in OpenClaw metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
