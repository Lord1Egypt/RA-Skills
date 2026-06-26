## Description: <br>
Error Detective helps developers investigate software failures by analyzing error context, stack traces, recurring patterns, performance symptoms, and likely root causes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtsatryan](https://clawhub.ai/user/mtsatryan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and reliability engineers use this skill to investigate application errors, classify failure patterns, analyze stack traces, and produce actionable debugging reports with evidence and confidence scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reused example code may read source files from stack-frame paths outside the intended project. <br>
Mitigation: Restrict file reads to the intended workspace and validate stack-frame paths before loading source snippets. <br>
Risk: Debug logs, source snippets, or investigation reports may expose sensitive data. <br>
Mitigation: Redact secrets and sensitive source or log content before sharing reports or storing examples. <br>
Risk: Example metrics or telemetry patterns could collect data unexpectedly if copied into a real project. <br>
Mitigation: Make telemetry explicit and opt-in, and document what data is collected before enabling it. <br>


## Reference(s): <br>
- [Error Detective code examples](references/examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/mtsatryan/ah-error-detective) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown investigation reports with root cause analysis, evidence, ranked solutions, code examples, and confidence scores.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The installed skill is markdown-only and does not execute code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
