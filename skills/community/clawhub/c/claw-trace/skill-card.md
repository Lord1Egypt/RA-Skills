## Description: <br>
Track and visualize the OpenClaw agent's work process by recording tool call inputs, outputs, duration, and status in an easy-to-read format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JDChi](https://clawhub.ai/user/JDChi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect OpenClaw tool activity, diagnose failed calls, summarize work progress, and optionally export trace reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic or persistent trace display could expose sensitive tool inputs or outputs. <br>
Mitigation: Keep tracing session-scoped and off by default around secrets, require explicit enablement, and redact credentials, tokens, private data, and file contents before display. <br>
Risk: Detailed logs or saved trace reports could persist sensitive information in the workspace. <br>
Mitigation: Leave detailedLog and saveToFile disabled unless needed, review generated reports before sharing, and remove or redact any sensitive content. <br>


## Reference(s): <br>
- [Claw Trace release page](https://clawhub.ai/JDChi/claw-trace) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown trace tables, flowcharts, statistics, detailed logs, and optional JSON or HTML exports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can run on demand or automatically when enabled; defaults keep detailed logging and file persistence disabled.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
