## Description: <br>
Upload videos to Bilibili with automatic login, title, description, tags, and partition selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iZorro](https://clawhub.ai/user/iZorro) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, operators, and developers use this skill to upload local video files to a Bilibili account with configurable metadata and partition IDs after a one-time interactive login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The upload workflow uses saved Bilibili login cookies after the user completes interactive login. <br>
Mitigation: Install and run the skill only on a trusted machine, and remove or revoke saved Bilibili cookies when automated uploading is no longer needed. <br>
Risk: An agent or script can publish a selected local video and metadata to the user's Bilibili account. <br>
Mitigation: Review the video path, title, description, tags, and partition ID before running an upload. <br>
Risk: The workflow depends on the external biliup package for login and upload behavior. <br>
Mitigation: Verify the biliup package source before installation or use. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a Python upload script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an interactive Bilibili QR-code login once; uploaded videos may be subject to Bilibili review.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
