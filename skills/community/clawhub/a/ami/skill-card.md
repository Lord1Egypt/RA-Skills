## Description: <br>
Ami is an IMA OpenAPI skill that helps an agent manage notes and knowledge-base content, including searching, reading, creating, appending, uploading files, and adding web links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aishaoqing](https://clawhub.ai/user/aishaoqing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to IMA notes and knowledge-base APIs for personal knowledge management tasks. It is intended for user-directed operations such as note lookup, note creation, appending to existing notes, knowledge-base search, file upload, and URL import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses user-provided IMA credentials to access notes, files, URLs, and knowledge-base content. <br>
Mitigation: Prefer environment variables or protected local configuration, and send credentials only to the official ima.qq.com API endpoint. <br>
Risk: The skill can create notes, append to existing notes, upload files, and import URLs, which may alter private user content. <br>
Mitigation: Ask for confirmation when the target note, knowledge base, or operation is ambiguous, and avoid exposing private note bodies in shared contexts. <br>
Risk: Incorrect encoding or file handling can corrupt note content or uploaded files. <br>
Mitigation: Validate UTF-8 before note writes, preserve original file bytes for knowledge-base uploads, run preflight checks, and use UTF-8 byte request bodies on PowerShell 5.1. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aishaoqing/ami) <br>
- [Publisher profile](https://clawhub.ai/user/aishaoqing) <br>
- [IMA homepage](https://ima.qq.com) <br>
- [IMA OpenAPI credential setup](https://ima.qq.com/agent-interface) <br>
- [Knowledge-base API reference](knowledge-base/references/api.md) <br>
- [Notes API reference](notes/references/api.md) <br>
- [Tencent Cloud COS authorization reference](https://cloud.tencent.com/document/product/436/7778) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown instructions with bash, PowerShell, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-provisioned IMA_OPENAPI_CLIENTID and IMA_OPENAPI_APIKEY credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
