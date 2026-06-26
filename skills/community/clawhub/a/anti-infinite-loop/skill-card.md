## Description: <br>
Anti-Infinite-Loop Guard helps agents detect repetitive execution cycles, enforce termination conditions, track progress, and reduce resource waste from infinite loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add lightweight loop-guard checks for repeated actions, iteration limits, timeouts, and basic progress checks during agent execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unexpected stopping behavior can interrupt legitimate long-running tasks. <br>
Mitigation: Review and tune max-iteration, timeout, repetition, and progress thresholds before using the guard in workflows where premature termination would be disruptive. <br>
Risk: Published performance metrics and watchdog claims are not independently verified by the security evidence. <br>
Mitigation: Treat the metrics as claims and validate behavior in the target agent environment before relying on them operationally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/anti-infinite-loop) <br>
- [Publisher profile](https://clawhub.ai/user/kofna3369) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit loop-stop reasons such as MAX_ITERATIONS_REACHED, TIMEOUT_EXCEEDED, and REPEATED_ACTION_DETECTED.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
