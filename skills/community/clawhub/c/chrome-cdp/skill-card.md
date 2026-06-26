## Description: <br>
chrome-cdp lets an agent inspect and operate already-open Chrome tabs through the Chrome DevTools Protocol, including logged-in and in-use page state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adminlove520](https://clawhub.ai/user/adminlove520) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to list, inspect, screenshot, navigate, click, type into, and evaluate JavaScript in live Chrome tabs when they need the agent to work with the user's existing browser state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and operate currently open Chrome tabs, including logged-in pages and sensitive in-use browser state. <br>
Mitigation: Use a separate Chrome profile with non-sensitive accounts, close private tabs before use, and grant access only when this live-browser capability is explicitly needed. <br>
Risk: The security evidence reports unsafe shell command construction around CDP command execution. <br>
Mitigation: Avoid running click, type, navigate, or eval operations on sensitive sites, and prefer a version that uses pinned helper code and safe argument passing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adminlove520/chrome-cdp) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/adminlove520) <br>
- [chrome-cdp-skill upstream project](https://github.com/pasky/chrome-cdp-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; runtime helper calls return JavaScript objects containing tab lists, screenshots paths, HTML, accessibility trees, network information, or command output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js 22+, Chrome with remote debugging enabled, and a local CDP helper script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
