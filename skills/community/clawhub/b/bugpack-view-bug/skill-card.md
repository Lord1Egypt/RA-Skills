## Description: <br>
View detailed bug context from BugPack including screenshots, environment info, and related files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[duhuazhu](https://clawhub.ai/user/duhuazhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect a specific BugPack bug before fixing it, including its description, priority, affected page, environment, screenshots, and related files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose bug details, screenshots, and source file paths returned by the local BugPack service. <br>
Mitigation: Use it only with a trusted local BugPack service and confirm the requested bug ID belongs to the current project. <br>
Risk: Related files and screenshots may influence where the agent looks next. <br>
Mitigation: Review the displayed context before using it to guide code inspection or repair work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/duhuazhu/bugpack-view-bug) <br>
- [BugPack local bug details endpoint](http://localhost:3456/api/bugs/:id) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Structured Markdown summarizing bug details, screenshots, environment information, and related files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only output based on the selected bug ID and the local BugPack service response.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
