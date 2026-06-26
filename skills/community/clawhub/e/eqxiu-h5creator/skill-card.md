## Description: <br>
易企秀H5制作 helps agents use the Eqxiu AIGC CLI to create and edit flip-style H5 pages from natural-language prompts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eqxiu](https://clawhub.ai/user/eqxiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to create invitation, poster, event, and other H5 pages with Eqxiu, return preview and edit links, and optionally adjust text or images. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses account tokens for Eqxiu API access. <br>
Mitigation: Avoid passing tokens directly on the command line, treat the saved token as sensitive, and rotate it if exposure is suspected. <br>
Risk: The skill can upload local files to Eqxiu/COS services. <br>
Mitigation: Upload only files the user explicitly wants to send to Eqxiu/COS and is comfortable sharing with those services. <br>
Risk: Activation may be broader than ideal for H5 generation and editing requests. <br>
Mitigation: Use the skill only when the user explicitly wants 易企秀 H5 generation, editing, image replacement, or material upload. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eqxiu/eqxiu-h5creator) <br>
- [HTTP API reference](references/http-api.md) <br>
- [Recommended workflow](references/workflow.md) <br>
- [Eqxiu token access](https://www.eqxiu.com/skillAccess/token) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return Eqxiu previewUrl, editUrl, scene IDs, editable text, image metadata, and upload results.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
