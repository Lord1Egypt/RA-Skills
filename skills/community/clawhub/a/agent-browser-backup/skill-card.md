## Description: <br>
A fast Rust-based headless browser automation CLI with Node.js fallback that enables AI agents to navigate, click, type, and snapshot pages via structured commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LoRexxar](https://clawhub.ai/user/LoRexxar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to let an agent automate browser workflows such as navigation, form filling, UI testing, data extraction, screenshots, recordings, and browser state management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can allow an agent to control authenticated browser sessions. <br>
Mitigation: Use test accounts or isolated browser sessions and avoid sensitive logged-in sites. <br>
Risk: Saved browser state files can contain sensitive session material. <br>
Mitigation: Treat saved state files like credentials and restrict where they are stored or shared. <br>
Risk: Screenshots, recordings, and traces can capture sensitive page content. <br>
Mitigation: Keep generated screenshots, recordings, and traces out of shared paths unless reviewed. <br>
Risk: Browser automation can perform consequential actions such as purchases, posts, deletes, uploads, or account changes. <br>
Mitigation: Require explicit approval before allowing the agent to take those actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/LoRexxar/agent-browser-backup) <br>
- [agent-browser CLI repository](https://github.com/vercel-labs/agent-browser) <br>
- [Agent Browser skill issue repository](https://github.com/TheSethRose/Agent-Browser-CLI) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documents optional JSON output from agent-browser commands for machine parsing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
