## Description: <br>
Bucket List helps users record, view, update, complete, cancel, review, import, and export a personal bucket list through a local JSON-backed CLI and localhost GUI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanguangzhe-collab](https://clawhub.ai/user/yanguangzhe-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to maintain a local personal bucket list, including adding wishes, changing their status, reviewing achievements, and managing JSON data through CLI or browser workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal bucket-list entries are stored in local JSON files and may contain sensitive goals or notes. <br>
Mitigation: Avoid entering secrets or highly sensitive information, and review the local data file before sharing, backing up, or publishing the workspace. <br>
Risk: Imported JSON or a linked file can replace or persist the current bucket-list data. <br>
Mitigation: Review JSON before importing it and link files deliberately because future saves can write the current list to the selected file. <br>
Risk: The optional life-progress widget stores birth year and life expectancy in the browser profile. <br>
Mitigation: Use the widget only if local browser-profile persistence of those values is acceptable. <br>


## Reference(s): <br>
- [Bucket List ClawHub page](https://clawhub.ai/yanguangzhe-collab/bucket-list) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown or plain text with shell commands and JSON file updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes and reads local bucket-list JSON data; the localhost GUI can import, export, and link a JSON file.] <br>

## Skill Version(s): <br>
1.4.0 (source: SKILL.md frontmatter, _meta.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
