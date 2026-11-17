## Description:

WebSocket-based cross-language communication service with support for multiple message types (text, JSON, dict, bytes, images, files, folders) and client management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build or operate WebSocket-based, cross-language messaging workflows that connect Python services with other clients, manage online clients, and transfer messages or files through Aliyun OSS when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose a WebSocket communication service on shared or remote networks without built-in access-control guidance.

Mitigation: Bind servers to localhost unless remote access is required, and add authentication, TLS, and sender restrictions before use on shared networks.

Risk: The skill supports automatic file, image, and folder transfer through Aliyun OSS and listener-triggered downloads.

Mitigation: Avoid broad auto-download listeners, quarantine and validate received files, and deliberately review any local files or folders before sending them to OSS.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wangyendt/skills/cross-comm)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and bash code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment configuration guidance for Aliyun OSS file transfer and async server/client usage examples.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
