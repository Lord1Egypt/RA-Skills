## Description: <br>
Cross-platform agent migration and deployment for moving OpenClaw agents, backing up and restoring agent state, deploying configurations across environments, and syncing workspaces between development and production. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haha8d](https://clawhub.ai/user/haha8d) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to migrate, back up, restore, and deploy OpenClaw agent state across local, server, WSL, and Docker environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exporting or syncing agent state can expose sensitive identity, memory, session, configuration, or credential data. <br>
Mitigation: Inspect the export contents, redact secrets and sensitive memory or session data, and use only trusted private repositories or transfer channels. <br>
Risk: Restoring an export or pull-mode backup can overwrite local OpenClaw files on the target machine. <br>
Mitigation: Create a separate backup of the target ~/.openclaw directory before restore and review repository contents before running restore scripts. <br>
Risk: The GitHub sync workflow can force-push to the remote branch. <br>
Mitigation: Remove or avoid the force-push path unless rewriting the remote branch is explicitly intended. <br>


## Reference(s): <br>
- [Docker Deployment Guide](references/docker-deploy.md) <br>
- [Agent Migrate ClawHub Page](https://clawhub.ai/haha8d/agent-migrate) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes migration, backup, restore, GitHub sync, rollback, and Docker deployment guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
