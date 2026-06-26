## Description: <br>
Better Memory installs and maintains a native OpenClaw memory stack with daily L1 logs, sidecar L2 summaries, weekly L3 rollups, migration support, and non-destructive review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuuuuujichaos](https://clawhub.ai/user/fuuuuujichaos) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to add durable workspace memory, capture typed memory entries, migrate legacy memory cautiously, and run daily, weekly, and monthly maintenance reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates durable workspace memory and managed blocks that can influence future agent behavior. <br>
Mitigation: Install it only in workspaces where persistent memory is intended, and review generated AGENTS.md and MEMORY.md managed blocks before relying on them. <br>
Risk: Scheduled maintenance or cleanup workflows could preserve, summarize, or change memory state in ways the user does not expect. <br>
Mitigation: Review .openclaw-memory-os sidecar files, migration plans, cleanup plans, and the cron template before enabling schedules or applying cleanup actions. <br>
Risk: Legacy memory migration may import outdated or low-confidence information into the new memory structure. <br>
Mitigation: Use the generated migration review and editable migration plan, and enable only the items that should be imported as candidate memory. <br>


## Reference(s): <br>
- [Better Memory V2 Schema](references/memory-schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/fuuuuujichaos/better-memory) <br>
- [Publisher Profile](https://clawhub.ai/user/fuuuuujichaos) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local Markdown, JSON, and text file artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and writes persistent workspace memory state under memory/, MEMORY.md, AGENTS.md managed blocks, and .openclaw-memory-os.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
