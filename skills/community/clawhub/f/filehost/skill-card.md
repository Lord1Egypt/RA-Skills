## Description: <br>
Upload files to lmfiles.com and return public download links via API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[setdemos](https://clawhub.ai/user/setdemos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to register for lmfiles.com access, upload files through the API, retrieve public download links, inspect file metadata, list account files, and delete uploaded files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded files become publicly reachable by anyone with the generated link. <br>
Mitigation: Confirm the file is intended for public sharing before upload and avoid uploading credentials, private documents, or sensitive data. <br>
Risk: LMFILES_API_KEY or LMFILES_BOOTSTRAP_TOKEN exposure could allow unauthorized account or file operations. <br>
Mitigation: Keep credentials in environment variables, avoid command-line token arguments where practical, do not paste secrets into shared logs, and rotate any exposed bootstrap token. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/setdemos/filehost) <br>
- [Publisher profile](https://clawhub.ai/user/setdemos) <br>
- [LMfiles documentation](https://lmfiles.com/docs) <br>
- [LMfiles OpenAPI schema](https://lmfiles.com/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API calls, Text] <br>
**Output Format:** [Markdown with inline bash commands and API response guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return public download links, file identifiers, metadata, account file lists, or deletion responses from lmfiles.com.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
