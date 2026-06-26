## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jau771](https://clawhub.ai/user/jau771) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to automate browser navigation, interaction, form filling, UI testing, screenshots, PDFs, recordings, and page data extraction through the agent-browser CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can operate on sensitive logged-in accounts and saved session files. <br>
Mitigation: Avoid using sensitive accounts unless necessary, treat auth state files and captured artifacts as secrets, and keep them out of logs and version control. <br>
Risk: Automated browser actions can submit forms, upload files, change account settings, post content, or make purchases. <br>
Mitigation: Supervise high-impact actions and review browser state before allowing the agent to proceed. <br>


## Reference(s): <br>
- [Agent Browser Jau771 ClawHub page](https://clawhub.ai/jau771/agent-browser-jau771) <br>
- [agent-browser CLI upstream repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON, Files] <br>
**Output Format:** [Markdown guidance with shell command examples; CLI output may include text, JSON, screenshots, PDFs, and recordings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and npm; browser automation can use saved state, cookies, local storage, screenshots, PDFs, and video artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
