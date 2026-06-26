## Description: <br>
Provides an agent-facing MCP server for authorized Canvas LMS users and observers to read courses, grades, assignments, announcements, planner items, conversations, and course files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, parents, observers, and agents acting for authorized Canvas users can use this skill to check coursework, grades, announcements, inbox conversations, calendar items, planner items, and linked student data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access Canvas account data, including observed-student data, through tokens, OAuth credentials, username/password credentials, or browser-session cookies. <br>
Mitigation: Use it only for Canvas accounts you control or are authorized to observe, prefer the most scoped official authentication option available, and avoid storing passwords or refresh tokens in shared configuration files. <br>
Risk: The fetchproxy browser-session fallback can reuse signed-in Canvas session cookies. <br>
Mitigation: Disable fetchproxy with CANVAS_DISABLE_FETCHPROXY=1 when browser-session cookie reuse is not intended. <br>
Risk: The skill can download course files to local disk. <br>
Mitigation: Download files only to a safe directory chosen for this purpose. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/canvas-parent-mcp) <br>
- [Canvas Parent MCP npm package](https://www.npmjs.com/package/canvas-parent-mcp) <br>
- [Fetchproxy extension](https://github.com/chrischall/fetchproxy) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown or text responses with JSON configuration and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May download Canvas course files to a user-selected local path.] <br>

## Skill Version(s): <br>
1.1.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
