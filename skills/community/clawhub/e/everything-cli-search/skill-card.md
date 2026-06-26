## Description: <br>
Search files and folders on Windows using Everything CLI with advanced filters, wildcards, regex, macros, sorting, and real-time indexing features. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dahanhstudio](https://clawhub.ai/user/dahanhstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Windows power users use this skill to install and operate Everything's es.exe CLI, compose advanced file-search queries, and use included wrappers to retrieve local file and folder search results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Bash wrapper constructs a command string and executes it with eval, which can execute unintended shell syntax if arguments are not trusted. <br>
Mitigation: Prefer direct es.exe or the Python wrapper; do not use scripts/es_search.sh until eval is removed and arguments are passed without shell re-evaluation. <br>
Risk: Administrative, deletion, reindexing, and remote server examples can affect files or expose indexed paths if followed carelessly. <br>
Mitigation: Treat destructive and administrative examples as manual actions requiring explicit confirmation; enable HTTP or ETP/FTP servers only on trusted networks with strong access controls and exclusions for sensitive folders. <br>


## Reference(s): <br>
- [Everything Documentation](https://www.voidtools.com/support/everything/) <br>
- [Everything Download](https://www.voidtools.com/) <br>
- [Everything Command Line Options](https://www.voidtools.com/support/everything/command_line_options) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Windows-focused guidance; requires Everything and es.exe to be installed and running for searches to work.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
