## Description: <br>
Systematic memory management for long-running AI agents using heartbeat, nightly, weekly, monthly, and yearly maintenance cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrewagrahamhodges](https://clawhub.ai/user/andrewagrahamhodges) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent operators and developers use this skill to install and run a recurring memory-maintenance system for long-running agents, keeping active memory concise while preserving decisions, lessons, commitments, archives, and yearly wisdom. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled autonomous memory maintenance can continue changing an agent's memory after installation. <br>
Mitigation: Run setup with --dry-run first, review the cron jobs before enabling them, and avoid --all unless administering every listed agent. <br>
Risk: Memory files may preserve sensitive personal or operational details over time. <br>
Mitigation: Keep passwords, tokens, credentials, addresses, and unnecessary personal details out of agent memory and review memory content before relying on it. <br>
Risk: Setup can modify MEMORY.md, HEARTBEAT.md, the memory directory, and scheduled jobs. <br>
Mitigation: Back up MEMORY.md and the memory directory before running setup. <br>


## Reference(s): <br>
- [Nightly Sleep Cycle Prompt](references/nightly-prompt.md) <br>
- [Weekly Reflection Prompt](references/weekly-prompt.md) <br>
- [Monthly Deep Clean Prompt](references/monthly-prompt.md) <br>
- [Yearly Wisdom Distillation Prompt](references/yearly-prompt.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and file-change instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory files and scheduled cron jobs when setup is run.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
