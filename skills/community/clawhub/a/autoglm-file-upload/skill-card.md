## Description: <br>
Use the AutoGLM Upload Mix API to upload local files such as images and documents, then obtain a file URL or resource ID for downstream API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khurramjamil12](https://clawhub.ai/user/khurramjamil12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to upload a selected local file to AutoGLM and capture the returned file URL or resource ID for downstream API workflows such as image recognition. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads a user-specified local file to AutoGLM, which can expose sensitive file contents if the wrong path is supplied. <br>
Mitigation: Confirm the exact file path before running the script and avoid using sensitive documents unless AutoGLM is trusted for that data. <br>
Risk: The upload flow depends on an authorization token from a local service at 127.0.0.1:18432. <br>
Mitigation: Use the skill only in environments where the local token provider is expected and trusted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/khurramjamil12/autoglm-file-upload) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with bash examples and JSON API response output from the upload script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints the AutoGLM upload response, including the file URL when the API returns oss_info.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
