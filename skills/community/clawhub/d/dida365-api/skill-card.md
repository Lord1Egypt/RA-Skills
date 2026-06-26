## Description: <br>
Dida365 滴答清单 (Open API) helps agents configure OAuth and use the Dida365 Open API to manage tasks and projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imchongliu](https://clawhub.ai/user/imchongliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Dida365 users use this skill to set up a Dida365 developer app, obtain an OAuth access token, and create, update, complete, delete, or organize tasks and projects through the official Open API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OAuth client secrets and the local Dida365 access token grant read/write access to the user's tasks and projects. <br>
Mitigation: Keep DIDA365_CLIENT_ID, DIDA365_CLIENT_SECRET, and ~/.config/dida365/token private, and do not commit them to version control. <br>
Risk: Delete, completion, and update operations can modify or remove Dida365 task and project data. <br>
Mitigation: Review generated API requests or commands before running them, especially for destructive or bulk operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imchongliu/dida365-api) <br>
- [Dida365 Developer Platform](https://developer.dida365.com) <br>
- [Dida365 Open API Base URL](https://api.dida365.com/open/v1/) <br>
- [Dida365 Help Center](https://help.dida365.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks and API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DIDA365_CLIENT_ID and DIDA365_CLIENT_SECRET environment variables plus a locally stored OAuth access token.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
