## Description: <br>
ClawDef is a self-hosted OpenClaw token optimization dashboard that tracks token usage, estimates costs, supports provider setup, manages budgets, detects waste, and can switch models locally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gs921302](https://clawhub.ai/user/gs921302) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to run a local dashboard for monitoring token usage, estimating model costs, managing provider setup, enforcing budgets, and adjusting model routing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill has sensitive OpenClaw administration powers, including model-routing changes. <br>
Mitigation: Install it only when administration is intended, review model provider configuration before use, and keep automatic optimization paused or disabled when model switching is not desired. <br>
Risk: Provider credentials used with the dashboard could affect spending or access if over-permissioned. <br>
Mitigation: Use limited-scope or budget-capped provider keys and keep budget limits aligned with expected usage. <br>
Risk: Local dashboard access controls protect administrative functions. <br>
Mitigation: Create and protect the first-run admin account, use strong credentials, and restrict local machine access to trusted users. <br>


## Reference(s): <br>
- [ClawDef ClawHub release page](https://clawhub.ai/gs921302/clawdef) <br>
- [Publisher profile](https://clawhub.ai/user/gs921302) <br>
- [ClawDef skill definition](artifact/SKILL.md) <br>
- [ClawDef security documentation](artifact/SECURITY.md) <br>
- [Node.js runtime](https://nodejs.org) <br>
- [Chart.js](https://www.chartjs.org) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local dashboard configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and operating guidance for a localhost OpenClaw monitoring dashboard.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
