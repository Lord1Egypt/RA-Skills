## Description: <br>
Queries the remaining hours of Alibaba Cloud Coding Plan using a command-line tool. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeeaay](https://clawhub.ai/user/jeeaay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators with Alibaba Cloud access use this skill to run a local helper that opens Alibaba Cloud, prompts login when needed, and reports Coding Plan usage percentages and reset times. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens Alibaba Cloud through agent-browser and may create or reuse a logged-in browser session. <br>
Mitigation: Run it only from a trusted directory, review AGENT_BROWSER_PATH and AGENT_BROWSER_SESSION_NAME values first, and close or delete the browser session when finished. <br>
Risk: The login flow can save a QR-code login screenshot as aliyu-login.png. <br>
Mitigation: Treat the screenshot as sensitive and delete it after login is complete. <br>
Risk: The helper depends on the external agent-browser command. <br>
Mitigation: Verify the installed agent-browser package and executable path before running the skill. <br>


## Reference(s): <br>
- [Coding Plan Usage on ClawHub](https://clawhub.ai/jeeaay/coding-plan-usage) <br>
- [agent-browser dependency](https://github.com/vercel-labs/agent-browser) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance and terminal output; successful runs emit usage JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save aliyu-login.png during login and reuse an agent-browser session.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
