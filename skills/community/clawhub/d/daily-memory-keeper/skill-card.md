## Description: <br>
Automatically organizes AI agent memory files by date, supports keyword retrieval and cross-session continuity, generates daily memory briefings, and cleans up expired data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to archive agent memory into a date-organized knowledge base, search prior memories by keyword, continue work across sessions, and receive daily memory summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Archived agent memories may persist secrets or highly sensitive information. <br>
Mitigation: Avoid storing secrets in agent memory, confirm the archive directory before use, and review stored memory content periodically. <br>
Risk: Memory recall can surface stale or incorrect context for important work. <br>
Mitigation: Review recalled memories before relying on them for consequential decisions or changes. <br>
Risk: Automatic cleanup or short retention settings can remove memory needed for later continuity. <br>
Mitigation: Set retention days and auto-clean behavior deliberately before enabling routine archiving. <br>


## Reference(s): <br>
- [Daily Memory Keeper on ClawHub](https://clawhub.ai/linbo405/daily-memory-keeper) <br>
- [linbo405 ClawHub publisher profile](https://clawhub.ai/user/linbo405) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, configuration, guidance] <br>
**Output Format:** [Markdown instructions, JSON configuration examples, archived knowledge-base files, retrieval results, and daily briefing text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses configurable archive directory, retention period, automatic cleanup, and daily briefing settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
