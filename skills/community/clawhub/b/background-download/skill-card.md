## Description: <br>
Asynchronous background download with retry, status tracking via Ontology, notifications to original channel. Supports resume on broken connections. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hansponddg](https://clawhub.ai/user/hansponddg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to start and monitor background file downloads, retry interrupted transfers, store task state in OpenClaw Ontology, and notify the original request channel when work completes or fails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Caller-controlled URLs and save paths can write untrusted content to local filesystem locations. <br>
Mitigation: Use only trusted callers and non-sensitive URLs; constrain downloads to an approved directory and validate URL schemes and paths before use. <br>
Risk: Shell command construction uses caller-controlled values for ontology, download, and notification operations. <br>
Mitigation: Harden command execution by avoiding shell=True or passing arguments as arrays, and reject unsafe URL, path, task ID, and channel values. <br>
Risk: Download URLs and local paths may be exposed in logs or completion and failure notifications. <br>
Mitigation: Redact sensitive URL and path details in messages and logs before broader deployment. <br>
Risk: Detached background tasks can linger, fail silently, or be difficult to cancel. <br>
Mitigation: Run zombie cleanup and archiving regularly, and add explicit cancellation or cleanup controls before use in higher-risk environments. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hansponddg/background-download) <br>
- [Publisher Profile](https://clawhub.ai/user/hansponddg) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Notifications] <br>
**Output Format:** [CLI text, JSON task records, downloaded files, and channel notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw Ontology and curl or wget; writes downloaded content to caller-provided filesystem paths.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
