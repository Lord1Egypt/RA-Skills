## Description: <br>
Daily cognitive training, dream review, dream-scene narration, and self-improvement loop for OpenClaw, Hermes, Codex, Claude Code, and other AI agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zrxparley](https://clawhub.ai/user/zrxparley) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to help agents record learning, run recall practice, connect concepts, review mistakes, generate dream-style consolidation reports, and plan the next improvement steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a persistent local cognitive-training store that may capture sensitive or unnecessary information if used carelessly. <br>
Mitigation: Keep the store project-local and do not record secrets, private transcripts, health details, or third-party personal data; store short redacted summaries instead. <br>
Risk: Optional scheduled reviews and memory-file updates can recur or change agent guidance beyond the current session. <br>
Mitigation: Enable scheduling only with user consent and review proposed edits to AGENTS.md, SOUL.md, MEMORY.md, CLAUDE.md, TOOLS.md, or copilot instructions before applying them. <br>


## Reference(s): <br>
- [Automation And Scheduling](references/automation.md) <br>
- [Dream Protocol](references/dream-protocol.md) <br>
- [Dream Styles](references/dream-styles.md) <br>
- [Storage Schema](references/storage-schema.md) <br>
- [Review Templates](references/templates.md) <br>
- [Training Protocols](references/training-protocols.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and local Markdown store files, with inline bash commands for initialization and scheduling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update project-local .cognitive-training files and an optional schedule.md after user consent.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
