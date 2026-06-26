## Description: <br>
Search, install, and export agentars and teams from the CatchClaw marketplace. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lovelcp](https://clawhub.ai/user/lovelcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use CatchClaw to search the CatchClaw marketplace, install individual agentars or teams, export local agents as distributable packages, and roll back workspace changes when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Install and rollback workflows can overwrite or replace local OpenClaw workspace content. <br>
Mitigation: Prefer named agent installs, require explicit confirmation before overwrite or team install actions, and use rollback only when the user intentionally wants to restore from a backup. <br>
Risk: Export can include local workspace content and can invoke OpenClaw enrichment unless skipped. <br>
Mitigation: Ask the user to choose the agent before export, exclude memory by default, review exported ZIP files for sensitive data, and use --skip-enrich when enrichment is not intended. <br>
Risk: Using latest-version behavior can install a different package version than the user expected. <br>
Mitigation: Use an explicit version when reproducibility matters and avoid --latest-style backup selection unless the target backup or package version is clear. <br>


## Reference(s): <br>
- [CatchClaw skill page](https://clawhub.ai/lovelcp/catchclaw) <br>
- [CatchClaw homepage](https://github.com/OpenAgentar/catchclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read or write local agent, team, backup, and export files when the user confirms the relevant command.] <br>

## Skill Version(s): <br>
3.7.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
