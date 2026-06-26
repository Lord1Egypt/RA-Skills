## Description: <br>
Continuous Learning helps an agent maintain long-term memory by syncing conversations to MemPalace, running scheduled memory analysis, extracting lessons into local documents, and recording corrective learnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[long57777](https://clawhub.ai/user/long57777) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add persistent memory workflows, scheduled reflection, and self-correction records to an OpenClaw-style agent workspace. It is intended for agents that need cross-session context and explicit learning files, with operator review of memory, document updates, and scheduled jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep broad long-term chat memory, which may include sensitive or regulated data. <br>
Mitigation: Review MemPalace contents before enabling the workflow, avoid storing secrets or regulated data, and periodically prune retained memory. <br>
Risk: Scheduled background jobs can sync and analyze memory without per-run review. <br>
Mitigation: Install scheduled tasks only when this behavior is intended, and regularly inspect or remove the OpenClaw Continuous Learning cron or task scheduler entries. <br>
Risk: MiniMax analysis and WeChat notification flows can send memory contents or summaries outside the local environment. <br>
Mitigation: Keep MiniMax and notification settings disabled unless those data flows are approved, and configure only approved API keys, recipients, and endpoints. <br>
Risk: The dream cycle can update core agent documents such as SOUL.md, AGENTS.md, MEMORY.md, TOOLS.md, and BOOTSTRAP.md. <br>
Mitigation: Back up core agent documents and review generated updates before relying on them in future sessions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/long57777/continuous-learning-kit) <br>
- [README](artifact/README.md) <br>
- [Bootstrap rules](artifact/bootstraps/bootstrap_rules.md) <br>
- [Dream configuration](artifact/config/dream_config.json) <br>
- [Documentation targets](artifact/config/documentation_targets.json) <br>
- [MiniMax API endpoint](https://api.minimax.chat/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python scripts, JSON configuration, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can initialize learning files, install scheduled jobs, queue notifications, read MemPalace entries, and append analyzed memory updates to local agent documents.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
