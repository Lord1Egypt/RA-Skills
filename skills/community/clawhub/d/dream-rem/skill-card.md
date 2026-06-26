## Description: <br>
Dream Rem consolidates daily memory logs into topic files, removes outdated or contradicted entries, and keeps MEMORY.md as a compact memory index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jofiction918](https://clawhub.ai/user/jofiction918) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to maintain local agent memory by periodically scanning recent daily logs, merging durable facts into topic files, pruning obsolete or conflicting entries, and rewriting the memory index. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can rewrite or delete local memory files while consolidating daily logs and topic files. <br>
Mitigation: Keep MEMORY.md, topics/, and memory/ under version control or backups, and review proposed file changes before enabling automated execution. <br>
Risk: Automated cron execution may repeatedly apply incorrect consolidation decisions if stale or contradictory memory entries are misclassified. <br>
Mitigation: Review execution reports and periodically audit the memory index, topic files, and heartbeat state after scheduled runs. <br>


## Reference(s): <br>
- [Dream Rem on ClawHub](https://clawhub.ai/jofiction918/dream-rem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown execution report with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update MEMORY.md, topic files, and memory/heartbeat-state.json when executed with file-write permissions.] <br>

## Skill Version(s): <br>
3.0.13 (source: server release metadata; artifact frontmatter says 3.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
