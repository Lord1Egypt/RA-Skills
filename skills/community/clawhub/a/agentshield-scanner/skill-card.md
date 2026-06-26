## Description: <br>
Scan AI agent skills, MCP servers, and plugins for security vulnerabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elliotllliu](https://clawhub.ai/user/elliotllliu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to run AgentShield checks on AI agent skills, MCP servers, plugins, archives, repositories, or packages before installation or release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to run an external npm CLI package. <br>
Mitigation: Install only if the package is trusted, pin the package version when possible, and scan only the specific skill, plugin, archive, repository, or package intended for review. <br>


## Reference(s): <br>
- [AgentShield Scanner on ClawHub](https://clawhub.ai/elliotllliu/agentshield-scanner) <br>
- [elliotllliu publisher profile](https://clawhub.ai/user/elliotllliu) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with shell command examples and JSON output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide threshold-based scans and JSON scanner output for programmatic review.] <br>

## Skill Version(s): <br>
0.5.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
