## Description: <br>
Manage OpenClaw agent configurations, update models, modify bindings, and test configuration changes with validation and rollback support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheben77](https://clawhub.ai/user/cheben77) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect, validate, and update OpenClaw agent configuration, including model assignments and channel bindings. It is also useful for testing configuration changes before applying them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration backups may copy sensitive OpenClaw settings to /tmp. <br>
Mitigation: Review backup file permissions, avoid sharing backup paths, and remove stale backups after confirming rollback is no longer needed. <br>
Risk: The documentation references helper scripts that are not bundled in this artifact. <br>
Mitigation: Verify a referenced script exists in the installed artifact before asking an agent to run it. <br>
Risk: Model or binding changes can route agent traffic differently than intended. <br>
Mitigation: Use validation or dry-run workflows first, review the proposed changes, and restart OpenClaw services only after approval. <br>


## Reference(s): <br>
- [Agent Config Manager on ClawHub](https://clawhub.ai/cheben77/agent-config-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local shell commands that read, validate, back up, or update OpenClaw configuration files.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
