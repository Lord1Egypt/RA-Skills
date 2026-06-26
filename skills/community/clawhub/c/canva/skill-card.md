## Description: <br>
Create, export, and manage Canva designs via the Connect API. Generate social posts, carousels, and graphics programmatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abgohel](https://clawhub.ai/user/abgohel) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, designers, and content teams use this skill to work with Canva designs from an agent, including listing designs, creating designs from brand templates, exporting files, uploading assets, and checking account context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read, create, upload, and export content through the connected Canva account. <br>
Mitigation: Use a Canva app or workspace with only the scopes needed, and confirm the design, file, template, and account context before approving operations. <br>
Risk: The skill depends on Canva client credentials and OAuth tokens stored on the local machine. <br>
Mitigation: Protect CANVA_CLIENT_SECRET and ~/.canva/tokens.json, keep token files private, and avoid sharing shell history or logs that may expose credentials. <br>
Risk: Uploads and exports can move local files or design data between the user's machine and Canva. <br>
Mitigation: Check file paths, design IDs, and exported download URLs before using them in downstream workflows. <br>


## Reference(s): <br>
- [Canva Connect API Docs](https://www.canva.dev/docs/connect/) <br>
- [Canva Developers](https://www.canva.com/developers/) <br>
- [Canva Connect API OpenAPI Spec](https://www.canva.dev/sources/connect/api/latest/api.yml) <br>
- [Canva Connect API Starter Kit](https://github.com/canva-sdks/canva-connect-api-starter-kit) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Canva API operations may return design metadata, export job status, asset upload responses, and download URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
