## Description:

FWQuant Skills provides a quant-analysis skill interface for strategy analysis, trading-signal requests, and basic result summaries for configured symbols and timeframes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuwenquant](https://clawhub.ai/user/fuwenquant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading workflow builders can use this skill to request quant-analysis style outputs for symbols, timeframes, and strategies. Reviewers should treat the current release as a limited stub rather than a complete trading, backtesting, or web dashboard system.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documentation presents broader trading, backtesting, and web dashboard capabilities than the artifact behavior demonstrates.

Mitigation: Treat this release as a limited quant-analysis stub and verify any trading, backtesting, or dashboard functionality before depending on it.

Risk: The documentation includes an example web host setting that could expose a future dashboard on a network interface.

Mitigation: If web service behavior is added, bind it to 127.0.0.1 by default and add authentication and firewall protections before exposing trading data or controls.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Structured text and Python dictionary output, with Markdown documentation and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, message, action context, symbol, timeframe, strategy, analysis text, and timestamp.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
