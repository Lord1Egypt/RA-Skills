## Description: <br>
Analyze error messages and logs to identify likely root causes of crashes, build failures, or runtime errors and suggest actionable fixes with code examples. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to triage pasted errors, stack traces, logs, and build failures, then receive a concise diagnosis with likely root cause, fix steps, and prevention guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted logs and stack traces may contain secrets, customer data, internal hostnames, or other sensitive values. <br>
Mitigation: Redact tokens, passwords, customer data, internal hostnames, and other sensitive details before using the skill or parser. <br>
Risk: Suggested fix commands or code snippets may be incorrect for the local environment if applied without review. <br>
Mitigation: Review proposed commands and code changes before execution, then test them in the target project or a safe environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown diagnosis with code snippets and optional JSON from the stack-trace parser] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured fields such as error type, message, frames, and suggested search queries when the bundled parser is used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
