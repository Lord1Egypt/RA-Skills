## Description: <br>
Anamnesis Hub helps OpenClaw agents set up persistent four-tier memory with local semantic retrieval, Markdown working memory, long-term archives, structured facts, optional cloud sync, and automated extraction pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[victorqr](https://clawhub.ai/user/victorqr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure persistent agent memory, local and optional cloud recall, automated extraction, synchronization, and maintenance scripts across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad persistent memory can capture conversations and retain sensitive context long term. <br>
Mitigation: Use only when persistent OpenClaw memory is intended; avoid secrets and regulated data, and disable conversation access unless needed. <br>
Risk: Cloud sync and external memory services can send local memory content outside the local environment. <br>
Mitigation: Review cloud sync destinations before enabling them and store MEMOS_API_KEY or other tokens carefully. <br>
Risk: Setup and pipeline scripts can edit OpenClaw configuration and schedule recurring jobs. <br>
Mitigation: Run dry-run modes first, inspect proposed openclaw.json and cron changes, and enable only the jobs required for the deployment. <br>
Risk: Cleanup, reset, or uninstall flows can affect memory and session files. <br>
Mitigation: Back up memory and session files before cleanup, reset, or uninstall commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/victorqr/anamnesis-hub) <br>
- [Documentation index](references/INDEX.md) <br>
- [Architecture](references/architecture.md) <br>
- [Setup guide](references/setup-guide.md) <br>
- [Memory directory](references/memory-directory.md) <br>
- [Sync API](references/sync-api.md) <br>
- [Scripts reference](references/scripts-reference.md) <br>
- [Pipeline stages](references/pipeline-stages.md) <br>
- [Candidates review](references/candidates-review.md) <br>
- [Upgrade and reset](references/upgrade-reset.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON snippets, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that may install plugins, edit OpenClaw configuration, schedule cron jobs, and operate on memory/session files.] <br>

## Skill Version(s): <br>
v1.13.2 (source: server release metadata; frontmatter 1.13.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
