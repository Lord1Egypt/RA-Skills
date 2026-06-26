## Description: <br>
DingTalk Docs management skill for reading, summarizing, creating, updating, and deleting DingTalk Docs and DingTalk knowledge-base documents through the DingTalk Open Platform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shyzhen](https://clawhub.ai/user/shyzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent retrieve, summarize, search, create, update, and delete DingTalk Docs when the user provides a DingTalk document link or an already established DingTalk Docs context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite and delete DingTalk documents. <br>
Mitigation: Require explicit human confirmation before overwrite or delete requests and review the target document before execution. <br>
Risk: The bundled whitelist allows workspace-wide writes with '/'. <br>
Mitigation: Replace the bundled whitelist with narrow workspace and document rules before installation, and avoid '/' unless every document in that workspace may be changed or deleted. <br>
Risk: The skill requires a DingTalk client secret. <br>
Mitigation: Keep DINGTALK_CLIENTSECRET protected and provide it only through the intended environment-secret mechanism. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/shyzhen/dingtalk-doc) <br>
- [DingTalk knowledge-base overview](https://open.dingtalk.com/document/development/knowledge-base-overview) <br>
- [DingTalk API Explorer](https://open-dev.dingtalk.com/apiExplorer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-shaped DingTalk API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DingTalk client credentials and sender identity; write operations depend on whitelist configuration.] <br>

## Skill Version(s): <br>
1.0.8 (source: ClawHub release evidence; artifact package.json reports 1.0.6) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
