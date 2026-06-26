## Description: <br>
Full-text search across all OpenClaw session logs using SQLite FTS5. Instant keyword search, topic queries, time-range filtering, and statistics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larios613-hub](https://clawhub.ai/user/larios613-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to index local session logs and retrieve past conversations by keyword, topic, time range, or session statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local search index can persist sensitive OpenClaw conversation history. <br>
Mitigation: Set SESSIONS_ROOT and SEARCH_AGENTS narrowly, avoid indexing logs that may contain secrets, and delete or protect scripts/search.db when finished. <br>
Risk: Search results may reveal private session content to anyone with local access to the tool output or database. <br>
Mitigation: Treat search output and the generated SQLite database as sensitive local data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/larios613-hub/fts5-session-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples, plus search result text from local SQLite queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and queries a local SQLite FTS5 index at scripts/search.db.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
