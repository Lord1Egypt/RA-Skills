## Description: <br>
Baidu Disk Manager helps agents manage Baidu Netdisk files through a local CLI, including login guidance, file listing, uploads, downloads, copies, moves, deletion, renaming, folder creation, quota checks, and JSON command output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[power-hayden](https://clawhub.ai/user/power-hayden) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to operate Baidu Netdisk content through go-bdisk commands. It is suited for listing files, checking quota, transferring files, and performing confirmed file changes in a personal Baidu Netdisk account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copy, move, rename, and delete operations can alter or remove Baidu Netdisk content. <br>
Mitigation: Show the operation type, source path, and target path before execution, then proceed only after the user explicitly replies with an accepted confirmation. <br>
Risk: Login requires account authorization and API credentials. <br>
Mitigation: Do not run login automatically; prompt the user to run the login command themselves and continue only after they confirm successful authentication. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/power-hayden/baidu-disk-manager) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented command output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands use go-bdisk with -j or --json for structured output when supported.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
