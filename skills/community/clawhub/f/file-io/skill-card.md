## Description: <br>
Uploads a user-selected local file to filebin.net and returns shareable file or bin links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to upload a specific local file to filebin.net for temporary link-based sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files are accessible to anyone with the generated filebin.net link while the bin exists. <br>
Mitigation: Confirm the exact file path before upload and avoid private, confidential, credential-containing, or regulated data. <br>
Risk: Large files may be rejected by filebin.net. <br>
Mitigation: Warn the user before uploading files larger than 100 MB and be prepared to stop or choose a different sharing method. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/file-io) <br>
- [filebin.net](https://filebin.net) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and filebin URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads the selected file to a public filebin.net bin and reports the resulting file and bin links.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
