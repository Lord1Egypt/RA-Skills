## Description: <br>
Repair damaged/corrupted files (video/document/design/archive) and provide an output download URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[water-star-creater](https://clawhub.ai/user/water-star-creater) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit a supported damaged file to Tenorshare 4DDiG Online Repair and receive a repaired-file download URL or, when requested, a local repaired-file path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected file is uploaded to Tenorshare 4DDiG and a presigned storage backend, which may expose personal or sensitive file contents to a third party. <br>
Mitigation: Ask for explicit consent before upload and avoid using the skill for confidential, regulated, or highly sensitive files. <br>
Risk: Download mode can write a repaired file to the user's local disk. <br>
Mitigation: Use download mode only when the user requests local output, then return the reported local path. <br>
Risk: Unsupported file types, oversized files, upstream repair failures, and local daily usage limits can prevent successful repair. <br>
Mitigation: Validate the file extension and size before execution, report upstream errors clearly, and recommend the official client when a documented limitation is reached. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/water-star-creater/file-repair) <br>
- [Tenorshare 4DDiG repair service](https://4ddig.tenorshare.com/video-repair.html?utm_source=clawhub.ai&utm_medium=partner&utm_campaign=4DDiG+File+Repair&utm_term=clawhubai-juni-product) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON result parsing notes; the repaired result is returned as a URL or local file path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create an optional local repaired-file output when download mode is requested.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata; artifact package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
