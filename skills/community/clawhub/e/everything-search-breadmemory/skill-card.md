## Description: <br>
Provides a Windows-focused local file search workflow using Everything/es.exe, plus breadcrumb knowledge storage, Ebbinghaus review scheduling, and topology-based knowledge association. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to search local Windows files by filename, turn selected results into concise local knowledge entries, review saved notes on an Ebbinghaus schedule, and explore relationships among stored notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill understates local file access, persistent knowledge storage, automation, and runtime executable download behavior. <br>
Mitigation: Install only when those behaviors are acceptable; prefer a manually verified es.exe, scope searches to explicit directories, and review or delete local data and backup files that may contain sensitive information. <br>
Risk: Search and knowledge workflows can expose local filenames, read matched files when used for summarization, and retain summaries or review metadata locally. <br>
Mitigation: Show search results before file parsing, avoid broad or scheduled ingestion until the scope is approved, and keep breadcrumb entries concise with links to original files rather than full sensitive content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/ldxs001/skills/everything-search-breadmemory) <br>
- [Everything by voidtools](https://www.voidtools.com) <br>
- [Workflow](references/workflow.md) <br>
- [Script reference](references/script-reference.md) <br>
- [Permissions](references/permissions.md) <br>
- [Data storage](references/data-storage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results may include local file paths; knowledge workflows can create local note, review, graph, and backup data.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release evidence, SKILL.md frontmatter, references/changelog.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
