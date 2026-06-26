## Description: <br>
Solve the "agent forgot everything" problem with search-first protocol, automated memory sync, and context preservation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up local memory files, search-first continuity rules, and scheduled synchronization so agents can preserve context across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files can store conversation context that may include sensitive user or project information. <br>
Mitigation: Use only in workspaces where local memory is acceptable, review memory files periodically, and avoid storing secrets or regulated personal data. <br>
Risk: Automated synchronization can add a recurring cron job that continues updating memory files. <br>
Mitigation: Inspect the crontab entry before enabling sync and remove the cron job when background memory updates are no longer wanted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Highlander89/agent-memory-continuity) <br>
- [SAPCONET homepage](https://sapconet.co.za) <br>
- [Memory continuity documentation](https://docs.sapconet.co.za/memory-continuity) <br>
- [Troubleshooting guide](docs/troubleshooting.md) <br>
- [Agent memory protocol template](templates/AGENT_MEMORY_PROTOCOL.md) <br>
- [Memory configuration](config/memory-config.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local memory protocol files and can enable recurring cron-based synchronization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
