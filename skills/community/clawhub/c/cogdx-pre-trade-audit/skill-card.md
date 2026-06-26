## Description: <br>
Verify trading reasoning with cognitive diagnostics before executing trades. Detects logical fallacies, calibration issues, and cognitive biases in your trade thesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drkavner](https://clawhub.ai/user/drkavner) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to audit prediction-market trade theses before execution. It returns a proceed, review, or reject recommendation and can optionally execute a trade when the audit passes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send trade reasoning to an external cognitive diagnostics service, which may expose proprietary strategies or sensitive reasoning text. <br>
Mitigation: Avoid sending secrets or proprietary strategies in reasoning text, and review external service use before installation. <br>
Risk: The skill can delegate trading authority when SIMMER_API_KEY is configured and live mode is enabled. <br>
Mitigation: Use dry-run first, set SIMMER_API_KEY only when live trading is intended, and require review before enabling live execution. <br>
Risk: The release includes scheduled managed automation that may run periodically if enabled. <br>
Mitigation: Disable or review the 15-minute scheduled automaton before deployment, especially in environments connected to trading credentials. <br>


## Reference(s): <br>
- [CogDx Pre-Trade Audit on ClawHub](https://clawhub.ai/drkavner/cogdx-pre-trade-audit) <br>
- [Cerebratech CogDx API](https://api.cerebratech.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Python dictionary or JSON containing the audit verdict, validity score, issues, recommendation, and trade outcome.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Dry-run by default; live trading requires explicit live mode and a SIMMER_API_KEY.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill metadata and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
