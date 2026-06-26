## Description: <br>
ClawTrace Runtime Observatory observes supplied AI workflow traces, reconstructs runtime call paths, and reports decisions, retries, fallbacks, critic activity, and context integrity without modifying the workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smallkeyboy](https://clawhub.ai/user/smallkeyboy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect AI workflow behavior from provided trace logs and runtime context, including nested skill calls, decision history, recovery paths, and missing-context diagnostics. It is intended for observation and explanation, not orchestration or automatic repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks to inspect full workflow traces and prior outputs, which can expose secrets, private prompts, personal data, or sensitive business context. <br>
Mitigation: Use it only where users and operators consent to trace inspection, and prefer host-side redaction, retention limits, and summary-only handling for sensitive workflows. <br>
Risk: Incomplete or unavailable trace logs can lead to misleading runtime explanations if the skill guesses missing workflow steps. <br>
Mitigation: Require complete trace logs for full reconstruction and preserve the documented trace-scoped retry behavior when logs are missing or incomplete. <br>


## Reference(s): <br>
- [ClawTrace Runtime Observatory on ClawHub](https://clawhub.ai/smallkeyboy/clawtrace-runtime-observatory) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON runtime trace report with concise diagnostic summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires supplied trace logs, previous output, data envelope, and debug-mode metadata; returns a trace-scoped retry request when required trace logs are missing.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
