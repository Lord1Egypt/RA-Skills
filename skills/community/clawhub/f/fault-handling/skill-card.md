## Description: <br>
Handles remote server fault operations by submitting run-script API jobs, polling execution history, and returning execution reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lerwee](https://clawhub.ai/user/Lerwee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations engineers use this skill to handle server incidents by confirming target hosts, running approved maintenance scripts such as service restarts or disk cleanup, and reviewing per-host execution results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad remote script-execution capability that may restart services or clean disks on servers. <br>
Mitigation: Install only for intended server operations, use least-privilege revocable API credentials, and require manual confirmation of exact hosts and script content before execution. <br>
Risk: Broad multi-host execution can amplify mistakes across infrastructure. <br>
Mitigation: Avoid broad multi-host runs unless explicitly approved and verified for the incident scope. <br>
Risk: Execution logs may contain sensitive operational output. <br>
Mitigation: Redact command output and host details before sharing reports outside the authorized operations context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lerwee/fault-handling) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON execution reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports include execution ID, task name, status, elapsed time, per-step details, per-host status, and captured stdout when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
