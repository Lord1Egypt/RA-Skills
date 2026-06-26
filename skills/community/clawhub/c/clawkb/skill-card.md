## Description: <br>
Use this skill when an agent needs to work with a ClawKB server over HTTP: register itself, obtain or use a Bearer token, upload images, create or update entries, search entries, read entry detail, or inspect plugin-backed API flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hata1234](https://clawhub.ai/user/hata1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use ClawKB to automate authenticated HTTP workflows for registering agents, uploading images, creating and updating knowledge entries, searching stored knowledge, reading entry details, and managing comments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bearer tokens or server URLs may be exposed through shared logs, repositories, or pasted command output. <br>
Mitigation: Use scoped, revocable tokens; avoid pasting tokens into shared logs or repositories; and rotate tokens if exposure is suspected. <br>
Risk: Create, update, upload, comment, and delete examples can change data on the target ClawKB server if executed. <br>
Mitigation: Confirm the base URL, token scope, target entry, and intended action before running write, delete, or upload commands. <br>
Risk: The optional auto-recall plugin can send conversation data to ClawKB and inject retrieved knowledge into agent context. <br>
Mitigation: Enable auto-recall only after reviewing its data flow, configuring per-sender token mappings, and confirming the ClawKB server is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hata1234/clawkb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide authenticated HTTP requests against user-provided ClawKB servers.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
