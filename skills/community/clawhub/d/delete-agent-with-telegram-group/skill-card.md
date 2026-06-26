## Description: <br>
Safely and thoroughly delete an OpenClaw agent and its artifacts, including workspace, agent files, bindings, Telegram group routing config, a dedicated Telegram group, and related cron jobs, with dry-run and explicit confirmation gates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sheetaa](https://clawhub.ai/user/Sheetaa) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to remove an OpenClaw agent and its related local files, routing configuration, cron jobs, and optionally a dedicated Telegram group after explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can permanently delete an OpenClaw agent and related local artifacts. <br>
Mitigation: Review the dry-run output, verify the agent ID, workspace path, Telegram group, and cron jobs, and approve execution only after confirming the intended targets. <br>
Risk: Deleting a Telegram group through browser or session control can be irreversible. <br>
Mitigation: Require separate explicit confirmation for Telegram group deletion, or use manual Telegram deletion if browser/session control is not acceptable. <br>
Risk: Accidental removal of configuration or scheduled jobs can affect recovery. <br>
Mitigation: Keep the generated backup files and review the final deletion summary before discarding recovery points. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sheetaa/delete-agent-with-telegram-group) <br>
- [Publisher profile](https://clawhub.ai/user/Sheetaa) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and concise status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run JSON output, backup file paths, deletion summaries, and Telegram group status values.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
