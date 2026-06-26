## Description: <br>
Use mcporter to call cpc-mcp-server AutoJS Agent tools for cloud Android task execution and result retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sav7ng](https://clawhub.ai/user/sav7ng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and QA engineers use this skill to dispatch AutoJS-based tasks to cloud Android devices, inspect cpc-mcp-server tools through mcporter, and retrieve task outputs such as screenshots, logs, or text results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can dispatch actions to cloud Android devices through a powerful external CLI and server. <br>
Mitigation: Review the target app, intended action, success criteria, and expected output before creating a task. <br>
Risk: A CLOUDPHONE_API_KEY grants access to the configured cloud-phone automation environment. <br>
Mitigation: Use a least-privilege key, prefer test accounts and non-production cloud phones, and never hardcode or commit real keys. <br>
Risk: mcporter full-URL and --stdio modes can broaden what the invocation reaches. <br>
Mitigation: Use the configured cpc-mcp-server with JSON --args by default, and use broader mcporter modes only when intentionally required. <br>


## Reference(s): <br>
- [Cloud Phone Agent on ClawHub](https://clawhub.ai/sav7ng/cloudphone) <br>
- [mcporter documentation](http://mcporter.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON argument examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter, cpc-mcp-server access, and CLOUDPHONE_API_KEY.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
