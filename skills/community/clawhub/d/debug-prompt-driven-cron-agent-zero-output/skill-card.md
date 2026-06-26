## Description: <br>
Helps agents troubleshoot prompt-driven cron or agentTurn tasks that complete successfully but produce zero samples or empty daily-review output, especially in Discord and Obsidian workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[can4hou6joeng4](https://clawhub.ai/user/can4hou6joeng4) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to distinguish successful-but-empty cron runs from sampling, filtering, or implementation-boundary failures. It guides evidence-based diagnosis of Discord sampling gaps, prompt-only agentTurn behavior, Obsidian output wording, Snowflake ID comparison, and timezone-window issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may lead an agent to inspect local OpenClaw cron logs, workspace files, and Obsidian notes that can contain private Discord or personal daily-review content. <br>
Mitigation: Constrain searches to the relevant job ID, task name, date window, and output files; avoid broad filesystem searches and redact sensitive message content in summaries. <br>
Risk: A successful cron run can be mistaken for proof that Discord retrieval and filtering were correct. <br>
Mitigation: Keep success status, retrieval coverage, and classification results separate; require evidence such as scanned channel or thread IDs, hit counts, and sample message IDs before treating a zero result as valid. <br>
Risk: Prompt-only cron tasks can leave critical sampling behavior to runtime model choices instead of a fixed implementation. <br>
Mitigation: Prefer explicit scripts or fixed toolchains for Discord sampling, with parent-channel scanning, thread-starter inclusion, thread reply scanning, string-based Snowflake comparisons, timezone-bounded queries, pagination, and audit logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/can4hou6joeng4/debug-prompt-driven-cron-agent-zero-output) <br>
- [Discord daily sampling contract](artifact/references/discord-daily-sampling-contract.md) <br>
- [Prompt agentTurn cron evidence boundaries](artifact/references/prompt-agentturn-cron-evidence-boundaries.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown troubleshooting guidance with inline paths, JSON snippets, text examples, and JavaScript-style comparison examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable payload; the skill may guide local searches over relevant logs, workspace files, and daily-note files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
