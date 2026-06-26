## Description: <br>
Standard protocol for reliable task dispatch, status reporting, and result feedback with confirmation, retry, and logging between agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nancliu](https://clawhub.ai/user/nancliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to standardize inter-agent task assignment, status updates, result reporting, acknowledgements, retries, and exception handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Communication logs may contain sensitive task details or secrets. <br>
Mitigation: Avoid putting secrets in messages, restrict log file permissions, and define retention or deletion rules for logged conversations. <br>
Risk: Agents may apply acknowledgement, retry, or exception-reporting steps inconsistently unless the protocol is adopted by all participants. <br>
Mitigation: Confirm participating agents use the documented message templates, timeout thresholds, and retry limits before relying on the protocol for coordination. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nancliu/agent-comm-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown communication protocol with reusable message templates and timeout tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes acknowledgement, retry, status-reporting, exception-reporting, and communication-log guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
