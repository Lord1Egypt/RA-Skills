## Description: <br>
Analyze and diagnose common programming error messages and stack traces with root causes and fix suggestions for Python, Node.js, Go, Bash, and system errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xueyetianya](https://clawhub.ai/user/xueyetianya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support agents use this skill to inspect local error messages, stack traces, or logs and receive concise explanations, likely causes, severity, and suggested fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Debugging suggestions can be incomplete or incorrect for a specific project or runtime environment. <br>
Mitigation: Treat the output as advisory, verify the diagnosis against the actual code and logs, and test fixes in a controlled environment before relying on them. <br>
Risk: Some suggested commands may require elevated privileges or change files, services, containers, or system settings. <br>
Mitigation: Review each privileged or mutating command before execution and run only the commands that match the user's environment and intent. <br>
Risk: Pasted or piped logs can contain secrets, tokens, hostnames, or other sensitive operational details. <br>
Mitigation: Redact sensitive values before analysis and avoid storing diagnostic output where unauthorized users can access it. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xueyetianya/debug-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Guidance] <br>
**Output Format:** [Terminal text with structured diagnostic sections, suggested shell commands, and short code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Bash and Python standard library; output is advisory and should be reviewed before acting on it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
