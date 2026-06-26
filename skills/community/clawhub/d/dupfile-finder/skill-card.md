## Description: <br>
Identify and list duplicate files in a specified directory to help manage and free up storage space. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and developers use this skill to scan a chosen local directory and identify files with matching SHA-256 content hashes so they can decide which duplicates to remove. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanning broad system or sensitive directories can expose file paths and take longer than expected. <br>
Mitigation: Point the tool at a specific folder and review the printed duplicate list before taking any cleanup action. <br>
Risk: The usage text names dupfile_finder.py while the artifact contains tool.py. <br>
Mitigation: Run the bundled tool.py file or rename it to match the usage text before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/albionaiinc-del/dupfile-finder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text file path listings with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prints duplicate file groups and their SHA-256 hashes; it does not delete files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
