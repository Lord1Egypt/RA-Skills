## Description: <br>
Create, deploy, host, and manage CMS-backed websites from the terminal using the FastMode CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arihgoldstein](https://clawhub.ai/user/arihgoldstein) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to create FastMode projects, define CMS schemas, manage content, validate website packages, deploy hosted sites, and invite clients to a portal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish or update live websites. <br>
Mitigation: Confirm the target FastMode project and approve deployments before they go live. <br>
Risk: The skill can change CMS schemas and content for existing sites. <br>
Mitigation: Review schema and content edits before applying them to an existing project. <br>
Risk: The skill can invite external users to client portals. <br>
Mitigation: Approve client invite links and permissions explicitly before they are shared. <br>
Risk: FastMode login credentials are stored locally after authentication. <br>
Mitigation: Log in only with the intended FastMode account and treat the local credential file as sensitive. <br>


## Reference(s): <br>
- [FastMode website](https://fastmode.ai) <br>
- [fastmode-cli npm package](https://www.npmjs.com/package/fastmode-cli) <br>
- [ClawHub skill page](https://clawhub.ai/arihgoldstein/fastmode) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and HTML/template code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands that create projects, edit CMS schemas and content, deploy live sites, manage client access, and store FastMode credentials locally.] <br>

## Skill Version(s): <br>
1.5.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
