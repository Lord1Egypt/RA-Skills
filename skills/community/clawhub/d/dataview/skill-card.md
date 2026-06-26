## Description: <br>
Dataview records and reviews local notes about data operations from the command line. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data practitioners use this skill to record local notes about data operations such as ingesting, transforming, querying, filtering, validating, and exporting activity logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is described as a CSV and JSON explorer, but security evidence says it behaves primarily as a local data-operation logbook. <br>
Mitigation: Use it for tracking operation notes rather than parsing or analyzing sensitive datasets, and verify expected behavior before relying on it for data exploration. <br>
Risk: Inputs are saved under ~/.local/share/dataview and may include sensitive notes, file paths, credentials, or dataset details. <br>
Mitigation: Avoid entering secrets, credentials, private dataset contents, or sensitive file paths unless local persistence is acceptable. <br>


## Reference(s): <br>
- [Dataview on ClawHub](https://clawhub.ai/bytesagain-lab/dataview) <br>
- [BytesAgain](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled command writes local timestamped logs and can export accumulated entries as JSON, CSV, or text.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
