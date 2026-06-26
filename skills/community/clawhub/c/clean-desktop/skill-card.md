## Description: <br>
Organizes Desktop files into image, document, and archive folders, with a preview mode before moving files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[578499893](https://clawhub.ai/user/578499893) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and desktop support agents use this skill to preview and organize Desktop files into common category folders without deleting files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move Desktop files into category folders, which may disrupt a user's preferred organization if run without review. <br>
Mitigation: Run dry_run first, review the exact proposed folders and file moves, and only allow a real run after the changes match the user's intent. <br>
Risk: Extension-based categorization may place files into broad folders that are technically correct but not what the user expects. <br>
Mitigation: Confirm the category mappings and generated move report before permitting file operations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain-text report with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports a dry_run preview before applying file moves.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
