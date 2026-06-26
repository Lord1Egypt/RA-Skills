## Description: <br>
Main orchestrator for the OpenAlgernon personal study system that starts study sessions, briefs the user, handles /algernon help, and routes study or content commands to companion sub-skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AntonioVFranco](https://clawhub.ai/user/AntonioVFranco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and learners using OpenAlgernon use this skill to begin study sessions, review available materials and progress context, and route study commands to the appropriate OpenAlgernon mode. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenAlgernon memory files and queries the local study database at session start. <br>
Mitigation: Install only when local OpenAlgernon study data is appropriate for the agent to read, and review the memory briefing before acting on it. <br>
Risk: The skill routes install, update, import, remove, audio, and ingest requests to companion sub-skills. <br>
Mitigation: Use explicit OpenAlgernon commands for content-management actions and review the companion sub-skills separately before relying on routed behavior. <br>
Risk: The skill depends on sqlite3 and an initialized OpenAlgernon database for due-card counts. <br>
Mitigation: Confirm sqlite3 is installed and the OpenAlgernon database is initialized before using the session-start briefing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/AntonioVFranco/algernon-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell commands and command-routing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads OpenAlgernon memory and study database state when starting a session; routes matched commands to companion OpenAlgernon skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
