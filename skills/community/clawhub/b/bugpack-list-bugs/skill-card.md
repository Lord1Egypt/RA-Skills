## Description: <br>
Lists tracked BugPack bugs with status and optional project filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duhuazhu](https://clawhub.ai/user/duhuazhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and project maintainers use this skill to query a local BugPack server and review tracked bug records grouped by status, with optional project filtering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bug titles and descriptions may include sensitive project details. <br>
Mitigation: Use the skill only in authorized contexts and avoid sharing displayed bug metadata outside the intended project audience. <br>
Risk: The skill depends on a local BugPack server at localhost:3456 returning expected bug metadata. <br>
Mitigation: Confirm the local server is the intended BugPack instance before use and treat unavailable or malformed responses as a data access issue rather than a successful bug listing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duhuazhu/bugpack-list-bugs) <br>
- [BugPack local bugs API](http://localhost:3456/api/bugs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown table or concise status-grouped list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bug identifiers, titles, descriptions, status, priority, project identifiers, and timestamps returned by the local BugPack server.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
