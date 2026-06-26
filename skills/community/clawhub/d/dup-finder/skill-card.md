## Description: <br>
Dup Finder identifies duplicate files in a selected directory by hashing file contents and listing matching paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local users use Dup Finder to scan a chosen directory for duplicate files before deciding what to remove or archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scanner reads and hashes every file under the directory the user selects. <br>
Mitigation: Run it only on directories you intend to inspect and avoid sensitive folders unless local content reading is acceptable. <br>
Risk: The README example uses a filename that does not match the packaged script. <br>
Mitigation: Run the packaged `tool.py` entrypoint or confirm the installed command name before scanning. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output listing duplicate file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads files under the selected directory locally and does not delete files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
