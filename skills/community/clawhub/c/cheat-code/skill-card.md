## Description: <br>
Cheat Code lets an agent call kenoodl.com for synthesis when it needs a new framing for an open-ended task. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kenoodl-synthesis](https://clawhub.ai/user/kenoodl-synthesis) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use Cheat Code to let an agent submit selected task context to kenoodl.com for synthesis when it is stuck, circling, or needs a new conceptual structure. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected prompts, task context, and agent reasoning may be sent to kenoodl.com for processing. <br>
Mitigation: Use the skill only with approved context and strip secrets, credentials, regulated personal data, confidential business material, and proprietary source context before calling the service. <br>
Risk: The required KENOODL_TOKEN authorizes access to the external service. <br>
Mitigation: Provide the token only through runtime environment or agent settings, avoid storing it in skill files, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kenoodl-synthesis/cheat-code) <br>
- [Publisher profile](https://clawhub.ai/user/kenoodl-synthesis) <br>
- [kenoodl](https://kenoodl.com) <br>
- [README](artifact/README.md) <br>
- [Agent instructions](artifact/instructions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON response snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires KENOODL_TOKEN and outbound HTTPS access to kenoodl.com.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata and claw.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
