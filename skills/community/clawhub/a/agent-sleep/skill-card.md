## Description: <br>
Agent sleep system for memory consolidation, log archival, workspace cleanup, and CortexGraph synchronization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guohongbin-git](https://clawhub.ai/user/guohongbin-git) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Agent Sleep to maintain long-running agents by checking memory state, consolidating logs, archiving daily notes, cleaning temporary files, and optionally syncing memory to CortexGraph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports broad scheduled cleanup behavior without enough safeguards. <br>
Mitigation: Review affected paths, deletion rules, backups, and sync destinations before enabling scheduling or running deep or CortexGraph flows. <br>
Risk: The security guidance calls out an undisclosed note-taking script that reads and writes a separate hard-coded notes file. <br>
Mitigation: Inspect or remove artifact/scripts/note.py unless the deployment intentionally allows access to that note file. <br>
Risk: Memory consolidation and synchronization can expose or move sensitive agent logs and long-term memory. <br>
Mitigation: Run the skill only in workspaces where memory contents, archives, and CortexGraph destinations are approved for the agent's data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guohongbin-git/agent-sleep) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or modify local memory, archive, and note files when its scripts are executed.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
