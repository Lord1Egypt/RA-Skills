## Description: <br>
Eidolon Search helps agents index and search markdown memory files with SQLite FTS5 so they can retrieve matching snippets instead of reading full files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dev-jsLee](https://clawhub.ai/user/dev-jsLee) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to build a local full-text index over markdown memory files, then run targeted keyword searches when full-file reading would be too expensive for the context window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cache benchmark helper may request sudo and clear Linux filesystem caches for the whole machine. <br>
Mitigation: Do not run the cache benchmark unless the operator understands the system-wide impact; prefer using only the index and search scripts for normal operation. <br>
Risk: SQLite FTS5 search is keyword-based and can miss results with typos, synonyms, semantic paraphrases, or complex conditions. <br>
Mitigation: Use specific keywords, phrase queries, OR-expanded synonyms, and follow up by reading matched files for full context. <br>


## Reference(s): <br>
- [Eidolon Search on ClawHub](https://clawhub.ai/dev-jsLee/eidolon-search) <br>
- [Publisher profile](https://clawhub.ai/user/dev-jsLee) <br>
- [Performance](references/PERFORMANCE.md) <br>
- [Search quality limitations](references/QUALITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and plain-text search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include matching snippets, file paths, and relevance scores from a local SQLite FTS5 database.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
