## Description: <br>
Automatically sorts files in a directory into folders named by file extension to help organize local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to organize a local directory by moving files into extension-named folders. It is useful for decluttering folders such as Downloads or Desktop while preserving files under the selected directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the sorter moves files and changes their paths, which can break shortcuts, scripts, or workflows that expect the old locations. <br>
Mitigation: Run it first on a test or backed-up directory and review the target path before execution. <br>
Risk: The documented command name may not match the packaged script name. <br>
Mitigation: Use the packaged script name if the documented command does not resolve. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/albionaiinc-del/filesorter-by-ext) <br>
- [Publisher profile](https://clawhub.ai/user/albionaiinc-del) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local filesystem changes by creating extension folders and moving files when the packaged script is run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
