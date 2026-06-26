## Description: <br>
Scans a local directory and reports files and their sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JayXu-D](https://clawhub.ai/user/JayXu-D) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and users invoke this skill to inspect an explicitly provided local folder path and receive a concise listing of files and their sizes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports an unsafe shell command path for invoking the helper script. <br>
Mitigation: Install only after review, use trusted explicit paths, and prefer a fixed version that uses native filesystem APIs or execFile/spawn with argument arrays. <br>
Risk: The release evidence reports undisclosed debug logging. <br>
Mitigation: Review runtime logging before use and prefer a version that removes debug logging or clearly discloses it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JayXu-D/folder-inspector) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text] <br>
**Output Format:** [Markdown table with file names, types, and sizes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the inspected path with the generated directory listing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
