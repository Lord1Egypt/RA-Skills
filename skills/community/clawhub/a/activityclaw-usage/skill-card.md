## Description: <br>
Guides agents in using the ActivityClaw plugin to inspect tracked file activity, command executions, web actions, messages, and sub-agent sessions through its status command and dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rmruss2022](https://clawhub.ai/user/rmruss2022) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to check what an agent has been doing, including file operations, shell commands, web activity, messages, and sub-agent sessions. It helps them open the ActivityClaw dashboard, check service status, control the local service, and troubleshoot missing activity data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: ActivityClaw records agent file activity, shell commands, web actions, messages, and sub-agent sessions into a local SQLite database and dashboard. <br>
Mitigation: Install and run it only when this level of local activity recording is acceptable, and stop the service when activity should not be recorded. <br>
Risk: The plugin is published by a third party, so users have supply-chain exposure when installing the npm package. <br>
Mitigation: Verify the package and repository before installation, and follow the security guidance from the server evidence. <br>


## Reference(s): <br>
- [ActivityClaw Plugin Usage on ClawHub](https://clawhub.ai/rmruss2022/activityclaw-usage) <br>
- [rmruss2022 ClawHub profile](https://clawhub.ai/user/rmruss2022) <br>
- [ActivityClaw GitHub repository](https://github.com/rmruss2022/ActivityClaw) <br>
- [ActivityClaw npm package](https://www.npmjs.com/package/@rmruss2022/activityclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference a localhost dashboard and local SQLite activity database when guiding ActivityClaw usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
