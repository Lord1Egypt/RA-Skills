## Description: <br>
Manage Docker stacks via the Portainer API, preserving environment variables during redeploys and using a one-shot redeployer for the default Claw stack. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaixi](https://clawhub.ai/user/zaixi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to update, redeploy, restart, or pull images for Docker stacks through Portainer while preserving stack environment variables. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Portainer-level access to manage Docker stacks, including redeploying stacks and restarting containers. <br>
Mitigation: Install only when the publisher is trusted, use a narrowly scoped Portainer API key when possible, and schedule production use during a maintenance window. <br>
Risk: The redeployer flow may expose the Portainer API key through redeployer container metadata or command content. <br>
Mitigation: Rotate the Portainer API key if redeployer container metadata may have exposed it, and remove stale redeployer containers after use. <br>
Risk: Cleanup logic force-deletes containers matching the claw-redep and ng-agent name patterns. <br>
Mitigation: Review the cleanup targets before running the skill in shared or production Docker environments. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell command examples and terminal status text from the management script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Portainer connection settings and a Portainer API key supplied through environment variables.] <br>

## Skill Version(s): <br>
5.1.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
