## Description: <br>
Migrate EasyClaw workspace-level behavior into a new OpenClaw workspace by locating and comparing old EasyClaw brain files such as AGENTS.md, SOUL.md, MEMORY.md, HEARTBEAT.md, memory/, launchd/context-management docs, then staging or importing them with backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sjingh](https://clawhub.ai/user/sjingh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inventory, stage, and selectively migrate legacy EasyClaw workspace memory, assistant instructions, context-management notes, and scheduling behavior into an OpenClaw workspace. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Legacy assistant memory can contain sensitive, stale, or unsafe instructions that become persistent if imported into the active OpenClaw workspace. <br>
Mitigation: Generate the report, stage files under imports/easyclaw/, and review staged memory and prompt files before making any content active. <br>
Risk: Running the memory import can replace the active OpenClaw MEMORY.md file. <br>
Mitigation: Use --import-memory only after review, retain the generated backup, and manually merge when additive migration is preferred. <br>
Risk: Legacy launchd and context-management automation may not map cleanly to the current OpenClaw environment. <br>
Mitigation: Treat old automation as reference material and rebuild wanted schedules explicitly as current heartbeat, cron, or workspace-script behavior. <br>


## Reference(s): <br>
- [EasyClaw Brain Migration Map](references/mapping.md) <br>
- [ClawHub skill page](https://clawhub.ai/sjingh/easyclaw-brain-migration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and staged file outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates a migration report and may stage copied EasyClaw files under imports/easyclaw/ before any active memory import.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
