## Description: <br>
Claw Memory Guardian helps OpenClaw users preserve local working memory through Markdown memory files, JSON indexes, backups, search, and Git-based save points. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BetsyMalthus](https://clawhub.ai/user/BetsyMalthus) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to initialize and maintain durable local memory for project notes, daily logs, searchable records, and recovery after interrupted sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates durable local memory files, backups, and Git history that may retain sensitive or regulated information. <br>
Mitigation: Do not store secrets, regulated data, or customer financial or contract details unless authorized and covered by a retention plan. <br>
Risk: The generated auto-save script can continue running in the background and repeatedly update local memory state. <br>
Mitigation: Run background auto-save only when the operator knows how to stop it and has reviewed the configured save interval. <br>
Risk: Git commits or workspace sharing can expose saved memory content beyond the local machine. <br>
Mitigation: Review Git status and repository contents before pushing, sharing, or publishing the workspace. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/BetsyMalthus/claw-memory-guardian) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [CLI text plus Markdown memory files, JSON index files, shell scripts, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates durable local files and may create Git commits in the OpenClaw workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
