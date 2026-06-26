## Description: <br>
Production-grade memory system for OpenClaw agents that organizes local Markdown notes, preserves context during compaction, and runs daily and weekly memory maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tzx666888](https://clawhub.ai/user/tzx666888) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create a local Markdown memory structure, split large MEMORY.md files into topic files, preserve key context before compaction, and schedule routine memory cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer makes persistent global OpenClaw configuration changes and adds scheduled background maintenance jobs. <br>
Mitigation: Review scripts/install.sh before running it, confirm the config changes and cron entries it will add, and keep or restore from the generated OpenClaw config backup if the behavior is not desired. <br>
Risk: Scheduled memory maintenance can process local memory files that may contain secrets, credentials, personal data, or private chat content. <br>
Mitigation: Define memory rules that exclude sensitive data before enabling the crons, and audit memory/ files regularly for content that should not be retained. <br>
Risk: Background cleanup and compaction behavior can change how an agent records and reuses context over time. <br>
Mitigation: Use openclaw cron list to review installed jobs, disable unwanted jobs with openclaw cron delete, and run scripts/verify.sh after installation or configuration changes. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tzx666888/beastxa-memory-pro) <br>
- [Quick Start](docs/quickstart.md) <br>
- [FAQ](docs/faq.md) <br>
- [Cron Prompt Templates](templates/cron-prompts.md) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local Markdown memory files and OpenClaw cron/configuration changes when the installer is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; changelog: v1.0.0 Initial release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
