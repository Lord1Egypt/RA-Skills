## Description: <br>
Manage Jimeng browser sessions with Playwright by importing cookies and browser storage so agents can access and automate Jimeng video generation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flyingzl](https://clawhub.ai/user/flyingzl) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to restore a saved Jimeng browser session, load Jimeng pages, capture screenshots, and automate video generation tasks that require authenticated browser state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses password-equivalent browser session data and can act inside a logged-in Jimeng account. <br>
Mitigation: Keep session JSON files out of source control, restrict file permissions, and delete session files after use. <br>
Risk: Automated browser actions may spend account credits or perform unintended actions if used outside the intended Jimeng workflow. <br>
Mitigation: Review the target URL and configured actions before running the helper, and scope use to the intended Jimeng pages. <br>
Risk: Screenshots and saved session artifacts may expose account or project information. <br>
Mitigation: Store screenshots and session files in controlled temporary locations and remove them when they are no longer needed. <br>
Risk: High-volume automation may trigger rate limiting or account restrictions. <br>
Mitigation: Use conservative delays, avoid proxy or rate-limit bypass behavior, and stop automation if the service challenges or blocks access. <br>


## Reference(s): <br>
- [Jimeng Session Data Usage Guide](references/jimeng-usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots and browser page information when the included Playwright helpers are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
