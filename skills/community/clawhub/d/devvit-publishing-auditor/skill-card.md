## Description: <br>
Audits Reddit Devvit apps for environment, configuration, compliance, and documentation readiness before publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asifdotpy](https://clawhub.ai/user/asifdotpy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers building Reddit Devvit apps use this skill to run a pre-publishing audit of CLI status, project configuration, source permissions, assets, and required documentation. It helps produce a Go / No-Go readiness report before server upload. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit may request project file scans or Devvit and TypeScript validation commands. <br>
Mitigation: Review each requested scan or command before approving it, especially any broader filesystem scan or global system change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asifdotpy/devvit-publishing-auditor) <br>
- [Publisher profile](https://clawhub.ai/user/asifdotpy) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown Go / No-Go report with command recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests user approval before validation commands, broad file scans, or suggested global system changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
