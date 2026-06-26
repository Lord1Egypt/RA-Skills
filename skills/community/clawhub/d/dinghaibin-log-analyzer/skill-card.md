## Description: <br>
Analyze log files to extract insights, errors, and patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect local application, access, JSON, or syslog-style logs for errors, warnings, regex matches, summary statistics, and optional JSON reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Log files may contain credentials, personal data, or other sensitive operational details. <br>
Mitigation: Review or redact logs before analysis and provide only files the agent should read. <br>
Risk: JSON reports can persist sensitive log excerpts or counts to disk. <br>
Mitigation: Write reports only to appropriate local paths and handle generated files according to the log data sensitivity. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dinghaibin/dinghaibin-log-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands] <br>
**Output Format:** [Plain text summaries, filtered log lines, or JSON reports from a local command-line analyzer.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a user-provided local log file and can write an optional JSON report to a user-chosen local path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
