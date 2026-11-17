## Description:

Run an AI-powered hedge fund simulation with 16+ investor-style agents that analyze stocks, report bullish, bearish, or neutral signals with confidence and reasoning, and aggregate a final BUY, SELL, or HOLD view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanjinlimkelvin-dot](https://clawhub.ai/user/tanjinlimkelvin-dot)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run a multi-agent stock-analysis simulation for selected tickers and review agent reasoning, confidence, and an aggregated portfolio-manager decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs mutable third-party code and modifies the Python environment during setup.

Mitigation: Use a virtual environment or container, pin and review the upstream repository commit, and avoid system-wide Python installation when possible.

Risk: The wrapper can read OpenClaw session configuration to select a model.

Mitigation: Specify an approved model explicitly with --model and avoid running prompts or provider settings that expose sensitive information.

Risk: Stock-analysis simulation output may be incorrect, stale, or misleading if treated as financial advice.

Mitigation: Use the output only as analysis support and require human review against trusted financial data before acting on results.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tanjinlimkelvin-dot/skills/ai-hedge-fund)
- [Upstream AI Hedge Fund Project](https://github.com/virattt/ai-hedge-fund)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [console text and markdown-style reasoning]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces per-agent stock signals, confidence scores, reasoning, and an aggregated BUY, SELL, or HOLD result.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
