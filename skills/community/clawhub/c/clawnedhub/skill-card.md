## Description: <br>
Security agent that inventories installed OpenClaw skills, analyzes them for threats, and syncs results to your Clawned dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jenish-sojitra](https://clawhub.ai/user/jenish-sojitra) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to inventory installed skills, scan selected skill directories for security issues, and sync metadata and results to a Clawned dashboard. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sync sends installed-skill inventory plus basic hostname and operating-system metadata to Clawned. <br>
Mitigation: Install only if you trust Clawned with that inventory and host metadata, and keep CLAWNED_SERVER set to the intended service. <br>
Risk: Explicit path scans read supported source files from the selected skill directory and send file contents for analysis. <br>
Mitigation: Avoid scanning directories that may contain secrets, and rely on the documented exclusion of .env files only as one control. <br>
Risk: Cron or watch mode can create ongoing synchronization behavior. <br>
Mitigation: Enable scheduled or watch operation only when continuous sync is intended. <br>


## Reference(s): <br>
- [Clawned homepage](https://clawned.io) <br>
- [Clawned API key settings](https://clawned.io/settings) <br>
- [ClawHub release page](https://clawhub.ai/jenish-sojitra/clawnedhub) <br>
- [Detection Patterns](references/detection-patterns.md) <br>
- [Threat Model](references/threat-model.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and JSON command output with Markdown setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWNED_API_KEY; optional CLAWNED_SERVER selects the Clawned service endpoint.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
