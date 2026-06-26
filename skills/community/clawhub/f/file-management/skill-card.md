## Description: <br>
Safe filesystem operations using built-in Unix tools and macOS utilities for listing, searching, reading, organizing, and managing files and directories while requiring confirmation before destructive operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tyronecoh](https://clawhub.ai/user/tyronecoh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they want an agent to inspect, search, organize, archive, move, copy, or delete local files with clear safety checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: File move, copy, archive, and delete commands can change or remove local data. <br>
Mitigation: Review the affected paths and exact proposed command before approval, and prefer recoverable deletion such as Trash on macOS when available. <br>
Risk: Broad searches or reads may expose sensitive files from local directories. <br>
Mitigation: Limit searches to the necessary paths and avoid scanning sensitive directories unless explicitly intended. <br>
Risk: Elevated filesystem operations can affect protected or shared system areas. <br>
Mitigation: Use elevated privileges only when explicitly requested and after confirming the target path and operation. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes read-only inspection first and explicit confirmation for write or destructive file operations.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
