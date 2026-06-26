## Description: <br>
Chrome MCP Tools helps agents access and control a live local Chrome browser through Chrome DevTools MCP middleware for opening pages, extracting rendered content, interacting with pages, taking snapshots, and collecting web data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mallocfeng](https://clawhub.ai/user/mallocfeng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when browser-rendered state is required, such as reading JavaScript-heavy pages, using an existing Chrome session, extracting article or list content, interacting with DOM elements, or capturing screenshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs external @mallocfeng/chromedev tooling that can control a live local Chrome session. <br>
Mitigation: Use only when the publisher and npm package are trusted, review install commands before execution, keep the endpoint bound to 127.0.0.1, and stop the daemon after use. <br>
Risk: A live Chrome session may already be logged into private accounts or sensitive sites. <br>
Mitigation: Prefer read-only tasks, avoid sensitive sites unless necessary, approve any Chrome debugging prompt deliberately, and limit extracted content to the requested task. <br>


## Reference(s): <br>
- [Chrome MCP Tools on ClawHub](https://clawhub.ai/mallocfeng/chromedev) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown or plain text with bounded extracted page content, summaries, and command snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local Chrome state through a daemon; final answers should be buffered, delivered once, and limited to the requested browser task.] <br>

## Skill Version(s): <br>
1.0.6 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
