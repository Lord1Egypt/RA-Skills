## Description: <br>
Lets an AI agent drive the local ClawHeart CLI for AI security auditing, skill review, agent discovery, MCP listing, provider profile listing, and credential governance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tjsdyy](https://clawhub.ai/user/tjsdyy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to ask an agent to run ClawHeart CLI checks and summarize local AI tooling, skills, agents, MCP servers, providers, and security findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad local security and credential-adjacent authority through ClawHeart CLI commands. <br>
Mitigation: Install it only when you intentionally want agent-driven ClawHeart scans, and treat provider, API-key, agent, and MCP output as sensitive. <br>
Risk: The artifact can direct users to run external installer commands when the CLI is missing. <br>
Mitigation: Review the external installer before running it and prefer a trusted ClawHeart installation path. <br>
Risk: Provider add/import/overwrite and init --reset workflows can change local configuration. <br>
Mitigation: Allow those actions only after an explicit user request and confirm the intended configuration change first. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tjsdyy/clawheart-security) <br>
- [ClawHeart website](https://clawheart.live) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON response handling] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries may include sensitive local security, provider, agent, and MCP configuration information.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
