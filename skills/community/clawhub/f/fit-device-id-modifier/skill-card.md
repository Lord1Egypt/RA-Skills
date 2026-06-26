## Description: <br>
Modifies FIT files so their device manufacturer and Garmin product IDs are recognized as Garmin Edge 500 China files by Garmin Connect. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CKboss](https://clawhub.ai/user/CKboss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technically comfortable users can run this local Python utility to convert third-party cycling FIT activity files into Garmin Edge 500 China device identity format for Garmin Connect recognition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The utility runs local Python code over personal FIT activity files. <br>
Mitigation: Install fitparse from a trusted Python environment, pass a specific file or directory, keep originals, and inspect generated _GM.fit files before uploading or sharing them. <br>
Risk: The utility changes device identity fields in copied activity files. <br>
Mitigation: Use it only when Garmin Edge 500 China identity is intended and verify Garmin Connect behavior on the generated copy before wider use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CKboss/fit-device-id-modifier) <br>
- [Publisher profile](https://clawhub.ai/user/CKboss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance, files] <br>
**Output Format:** [Markdown guidance with Python command examples; execution creates modified FIT file copies.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates new files with a _GM.fit suffix, preserves original FIT files, skips previously processed outputs, and recalculates FIT CRC values.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
