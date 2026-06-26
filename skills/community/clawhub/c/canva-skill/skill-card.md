## Description: <br>
Create, export, upload assets to, and manage Canva designs via the Canva Connect API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiangwill2023](https://clawhub.ai/user/jiangwill2023) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Canva users use this skill to guide agents through Canva Connect API workflows for creating designs, exporting files, listing designs, uploading assets, and autofilling brand templates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires Canva OAuth credentials and stores access tokens locally. <br>
Mitigation: Keep CANVA_CLIENT_SECRET and ~/.canva/tokens.json private, restrict token-file permissions, and grant only the scopes needed for the task. <br>
Risk: The skill can upload local files and perform design-management actions through Canva. <br>
Mitigation: Confirm exact local files before upload and review write, autofill, export, or batch actions before running them. <br>


## Reference(s): <br>
- [Canva Developers](https://www.canva.com/developers/) <br>
- [Canva Connect API](https://api.canva.com/rest/v1) <br>
- [Canva Skill on ClawHub](https://clawhub.ai/jiangwill2023/canva-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Canva OAuth credentials and appropriate Canva API scopes before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
