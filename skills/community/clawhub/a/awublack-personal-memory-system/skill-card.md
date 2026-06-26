## Description: <br>
Awublack Personal Memory System syncs a user's MEMORY.md notes into SQLite and helps an agent query them in natural language, with documented Obsidian and Git synchronization for redundancy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awublack](https://clawhub.ai/user/awublack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to maintain a personal, queryable memory base from local Markdown notes and retrieve prior thoughts or decisions through an assistant. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security summary says the documented background Git sync may push private personal notes to a remote repository while the skill also describes local-only storage. <br>
Mitigation: Review git_sync_on_save.sh before starting it, confirm the exact repository and files it will push, and avoid storing secrets or highly sensitive notes in MEMORY.md. <br>
Risk: The artifact uses hard-coded workspace paths under /home/awu, so the scripts may fail or access unintended files outside that expected environment. <br>
Mitigation: Inspect and adapt local paths before installation, then verify MEMORY.md, memory.db, the Obsidian vault, and sync logs point to the intended workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/awublack/awublack-personal-memory-system) <br>
- [Publisher profile](https://clawhub.ai/user/awublack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Natural-language answers and Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries local SQLite memory records derived from MEMORY.md; setup depends on user-specific local paths and optional Git synchronization.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
