## Description:

Detects structural macro regime transitions over a 1-2 year horizon using cross-asset ratios across concentration, yield curve, credit, size, equity-bond, and sector rotation signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to assess current macro or market regime transitions, structural rotation, and long-term positioning signals from cross-asset market data. It is intended for general market commentary rather than personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market posture output could be mistaken for personalized financial advice.

Mitigation: Present findings as general market commentary and require human review before using them for investment decisions.

Risk: API keys may be exposed if passed directly on the command line.

Mitigation: Prefer setting FMP_API_KEY in the environment and avoid logging or sharing commands that include credentials.

Risk: The artifact README mentions a Yahoo Finance command that server security guidance flags as unsupported.

Mitigation: Use the documented FMP API path unless the alternate data source is fixed and revalidated.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/clawdiri-ai/skills/einstein-research-regime-dv)
- [Regime Detection Methodology](references/regime_detection_methodology.md)
- [Indicator Interpretation Guide](references/indicator_interpretation_guide.md)
- [Historical Regime Examples](references/historical_regimes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Natural-language analysis plus generated Markdown and JSON report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires market data access through FMP_API_KEY or an explicit API key; generated reports are timestamped local files.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
