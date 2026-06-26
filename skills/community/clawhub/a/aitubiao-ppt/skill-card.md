## Description: <br>
Generates editable PPT presentation projects from a topic, pasted text, or supported file by using the aitubiao API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aitubiao](https://clawhub.ai/user/aitubiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create, review, edit, and optionally export aitubiao PPT projects from supplied presentation content. The workflow includes credential setup, quota and fee confirmation, project creation, and result handoff through a project URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to paste an aitubiao API key into chat. <br>
Mitigation: Use a restricted or temporary API key when possible, revoke it after use if supported, and avoid sharing keys outside the intended local setup flow. <br>
Risk: The API key is stored locally for later sessions. <br>
Mitigation: Review local credential storage, remove credentials when no longer needed, and rotate the key if the machine or chat transcript may be exposed. <br>
Risk: The bundled CLI can perform broader aitubiao actions than PPT creation. <br>
Mitigation: Review commands before execution and limit use to the requested PPT workflow unless the user explicitly requests supported follow-up actions. <br>
Risk: PPT generation can consume account credits or create duplicate charges if repeated after timeout or server errors. <br>
Mitigation: Confirm quota and fees before creation, do not automatically retry non-retryable create calls, and ask the user before starting a new generation attempt. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aitubiao/aitubiao-ppt) <br>
- [Aitubiao App](https://app.aitubiao.com) <br>
- [Aitubiao API Key Management](https://app.aitubiao.com/setting/api-keys?utm_source=skill_skill-clawhub&channel=skill-clawhub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON request bodies; successful runs return project links and optional downloaded files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access to api.aitubiao.com, Bash, curl, jq, and an aitubiao API key stored locally for later sessions.] <br>

## Skill Version(s): <br>
1.2.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
