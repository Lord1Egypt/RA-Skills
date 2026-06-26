## Description: <br>
Guides agents through using the file_crypto SDK to encrypt or decrypt server-local files and retrieve Agent authId tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loofare](https://clawhub.ai/user/loofare) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to guide single-file or batch encryption and decryption of files already present on a server, and to obtain the authId needed by the file_crypto command-line flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security review flagged unclear remote backend use and possible exposure of a reusable authId token in chat. <br>
Mitigation: Review what backend service is contacted and what file data or metadata is sent before installing; treat authId values as secrets and keep them out of shared chats, logs, screenshots, and issue reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loofare/file-crypto) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports command results, target file paths, and error-handling guidance; does not produce encrypted file contents directly.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
