## Description: <br>
This skill helps agents batch rename files using sequential numbering, find and replace, prefix or suffix insertion, regular expressions, extension filters, and optional recursive folder processing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1227323804](https://clawhub.ai/user/1227323804) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users can use this skill when they need an agent to plan and run repeatable file renaming operations across a specified folder. It is suited for organizing images, documents, and other local files with predictable naming patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files are renamed in place, which can be difficult to undo after execution. <br>
Mitigation: Ask the agent for an exact old-to-new filename preview, test on a small folder first, and back up important files before running the command. <br>
Risk: Recursive operation can affect more files than intended. <br>
Mitigation: Use non-recursive mode unless subfolder processing is required, and constrain the scope with an extension filter where possible. <br>
Risk: Incorrect find-and-replace or regex patterns can produce unexpected filenames. <br>
Mitigation: Review the rename pattern and previewed mappings before execution, especially for regex-based renames. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/1227323804/batch-rename-1) <br>
- [Publisher Profile](https://clawhub.ai/user/1227323804) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and execution summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script prints renamed file mappings and a JSON summary after execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
