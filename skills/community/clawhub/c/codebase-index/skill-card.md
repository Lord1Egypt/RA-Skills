## Description: <br>
Scans project directories, extracts Python symbols and imports, and builds a searchable JSON codebase index. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxr-666](https://clawhub.ai/user/lxr-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to create a local index of a project, then query symbols, files, and statistics while exploring or maintaining a codebase. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated JSON index may contain sensitive code metadata such as file paths, docstrings, imports, symbol names, and limited variable value representations. <br>
Mitigation: Run the indexer only on intended project directories and treat generated index files as sensitive project artifacts. <br>
Risk: The skill reads local project files and writes an index file selected by the user. <br>
Mitigation: Review scan targets and output paths before running the commands, especially in workspaces that contain private or regulated code. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxr-666/codebase-index) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands; generated indexes are JSON and query results are terminal text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3. The indexer runs locally and does not require network access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
