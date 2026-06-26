## Description: <br>
Browser-driven web research and live site inspection using Chrome DevTools MCP over a remote-debugging Chrome session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hackerchai](https://clawhub.ai/user/hackerchai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to inspect live websites, search engines, social platforms, documentation, dashboards, and login-aware or JavaScript-heavy pages, then cross-check and summarize findings from visible page state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent control and inspect a live Chrome session, exposing tabs, cookies, logins, and page state. <br>
Mitigation: Use a separate temporary Chrome profile with no sensitive accounts, close unrelated tabs, avoid authenticated pages unless truly needed, require confirmation before form submissions or account-changing actions, and turn off remote debugging when finished. <br>


## Reference(s): <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [ClawHub skill page](https://clawhub.ai/hackerchai/chrome-devtools-web-research) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured source-quality summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser-visible findings, source-quality grouping, caveats, and remediation steps.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
