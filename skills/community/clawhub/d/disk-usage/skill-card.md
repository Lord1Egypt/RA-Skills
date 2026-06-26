## Description: <br>
Shows disk usage for a directory or file in human-readable format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jinwangmok](https://clawhub.ai/user/jinwangmok) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and other users can check how much space a directory or file uses and identify the largest items in a directory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Disk usage output can reveal directory names, file names, and project structure. <br>
Mitigation: Avoid running the skill on sensitive directories when path names or child item names should remain private. <br>
Risk: The script reports an error for paths that are not directories. <br>
Mitigation: Use a directory path with the bundled script, or use the documented direct du command when checking a single file. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jinwangmok/disk-usage) <br>
- [Publisher profile](https://clawhub.ai/user/jinwangmok) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text with human-readable disk sizes and paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runnable script accepts one optional directory path and prints the top 20 child items by size followed by the total.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
