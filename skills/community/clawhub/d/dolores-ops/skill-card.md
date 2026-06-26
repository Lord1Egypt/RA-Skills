## Description: <br>
Dolores 运维工具 helps an OpenClaw assistant perform routine operations including health checks, memory sync, workspace cleanup, log management, and scheduled task management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[milesnee](https://clawhub.ai/user/milesnee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to ask an OpenClaw assistant to check its runtime health, inspect logs and workspace files, synchronize memory notes, clean temporary files, and manage recurring maintenance tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local OpenClaw commands and inspect logs or workspace files. <br>
Mitigation: Review proposed commands and file targets before execution, especially for cleanup or operational changes. <br>
Risk: The skill includes recurring memory synchronization that may retain conversation-derived information. <br>
Mitigation: Require explicit approval for memory sync when appropriate and periodically review stored memory files. <br>
Risk: The skill can help create scheduled tasks that may repeat maintenance actions automatically. <br>
Mitigation: Confirm cron task details before creation and keep task IDs visible for later review or removal. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/milesnee/dolores-ops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown status summaries with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local maintenance actions such as cleanup, memory writes, log inspection, and cron changes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
