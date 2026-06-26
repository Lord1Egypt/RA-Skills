## Description: <br>
Searches a local document library such as an Obsidian vault, wiki, notes folder, or documentation set using BM25 query matching, LLM query expansion, and grep for line-level locations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[FantasyRL](https://clawhub.ai/user/FantasyRL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and knowledge workers use this skill to search local notes and documentation, narrow results to likely files, and report matching file paths with line numbers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads and indexes a user-selected local document folder, so choosing a broad directory can include unrelated or sensitive files. <br>
Mitigation: Point the skill at a specific notes or documentation directory and avoid sensitive unrelated folders. <br>
Risk: The generated search index may contain content-derived metadata from local documents. <br>
Mitigation: Keep the index local and avoid syncing or sharing it unintentionally. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/FantasyRL/doc-search) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON search-result arrays] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include path, relative path, score, title, and summary fields; final reporting can include grep line numbers.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
