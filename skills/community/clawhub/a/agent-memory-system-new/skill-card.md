## Description: <br>
Helps OpenClaw agents maintain persistent local memory with hot, warm, and cold storage, scheduled archiving, nightly reflection, and skill extraction from lessons. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Tomor1984](https://clawhub.ai/user/Tomor1984) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to set up a local memory workspace for OpenClaw agents, keep daily logs and lessons organized, archive older memory files, and generate reusable skill scaffolds from recorded lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The installer can add recurring background jobs for garbage collection and nightly reflection. <br>
Mitigation: Review the proposed crontab entries before enabling automation, and skip or remove scheduled jobs when persistent background maintenance is not desired. <br>
Risk: Maintenance scripts can move or replace local workspace memory files. <br>
Mitigation: Run garbage collection with --dry-run first, confirm the WORKSPACE path, and keep backups of important memory files before enabling scheduled runs. <br>
Risk: Persistent memory files may expose sensitive personal or business information to future agents. <br>
Mitigation: Avoid storing sensitive data in the memory directory unless future agent access is intended and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Tomor1984/agent-memory-system-new) <br>
- [Tomor1984 publisher profile](https://clawhub.ai/user/Tomor1984) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples, shell scripts, and memory template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains local memory files, archive reports, reflection records, and generated skill scaffolds in the configured workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
