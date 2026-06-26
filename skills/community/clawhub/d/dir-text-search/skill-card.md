## Description: <br>
Searches for text or regex patterns recursively in directories and supported archive formats, including ZIP, RAR, TAR, and 7z. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[trylovecatch](https://clawhub.ai/user/trylovecatch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, support engineers, and operators use this skill to find strings or regex matches in logs, configuration files, source files, and compressed archives. It helps an agent run the bundled search script, locate the generated result file, and summarize matching files and lines for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Matched lines are copied into plaintext result files, which can expose secrets, credentials, or personal data found in searched files. <br>
Mitigation: Run the search on specific folders, review the result file before sharing it, and delete generated results that contain sensitive content. <br>
Risk: Broad searches can collect more local file content than intended. <br>
Mitigation: Use a narrow target path and avoid scanning an entire home directory unless that scope is intentional. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/trylovecatch/dir-text-search) <br>
- [RARLAB UnRAR downloads](https://www.rarlab.com/rar_add.htm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and plaintext search result files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results are written to timestamped plaintext files under search_results/ unless a different output directory is provided.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
