## Description: <br>
Manage Duplicati backups on the server using secure Bearer tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robnew](https://clawhub.ai/user/robnew) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to let an agent monitor Duplicati server state, list backup jobs, start a selected backup, and retrieve recent failure logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authenticated access to a Duplicati server through a bearer token. <br>
Mitigation: Protect the token, avoid committing configuration files containing it, prefer a shorter-lived or revocable token when supported, and restrict the Duplicati API to trusted networks. <br>
Risk: The agent can start backup jobs, so a mistaken job name or ID could trigger the wrong backup. <br>
Mitigation: List and match backup jobs before starting one, and confirm the resolved backup name or ID before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robnew/duplicati-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise status or log summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DUPLICATI_URL and DUPLICATI_TOKEN; output may include backup job IDs, phase descriptions, destination free-space notes, and recent error-log summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
