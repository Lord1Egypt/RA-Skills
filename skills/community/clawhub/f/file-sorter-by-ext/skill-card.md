## Description: <br>
Automatically organizes files into folders by their extension within a specified directory to keep files systematically sorted. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[albionaiinc-del](https://clawhub.ai/user/albionaiinc-del) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to organize local directories by moving files into extension-named folders from the current directory or a specified path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool moves files in-place and can reorganize a directory unexpectedly if run in the wrong location. <br>
Mitigation: Run it only in a directory intended for sorting, and back up important files or test on a copy first. <br>
Risk: The usage text names file_sorter_by_ext.py, while the artifact provides tool.py. <br>
Mitigation: Run the included tool.py file unless the package maintainer supplies a matching wrapper script. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/albionaiinc-del/file-sorter-by-ext) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Moves files in-place into extension-named folders; no generated content is intended for downstream model training or automated decision-making.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
