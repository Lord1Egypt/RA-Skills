## Description: <br>
Uploads a local file to Qiniu Cloud Storage and returns a shareable URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahsbnb](https://clawhub.ai/user/ahsbnb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and users who need to share non-sensitive local files can upload a selected file to a configured Qiniu Kodo bucket and receive a public URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files may become publicly accessible depending on Qiniu bucket configuration. <br>
Mitigation: Use the skill only for non-sensitive files and verify bucket access settings before uploading. <br>
Risk: Broad or incorrect Qiniu credentials could expose more storage access than intended. <br>
Mitigation: Use credentials scoped to the intended bucket and confirm the configured public domain before use. <br>
Risk: The skill depends on the external qiniu Python package. <br>
Mitigation: Install qiniu from a trusted package source and pin or review the package version in controlled environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ahsbnb/file-to-link) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text URL on standard output, with errors reported on standard error.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the qiniu Python package and configured Qiniu bucket, domain, and credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
