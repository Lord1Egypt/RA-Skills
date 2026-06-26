## Description: <br>
AI-powered code review assistant for OpenClaw agent developers that analyzes code quality, detects security and performance issues, and provides actionable improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[supermario11](https://clawhub.ai/user/supermario11) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to review local codebases for security vulnerabilities, performance bottlenecks, code smells, best-practice gaps, and documentation quality. It is especially aimed at OpenClaw agent and skill projects where review findings are turned into terminal summaries or Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the local files or directories selected for review. <br>
Mitigation: Install and run it only when local code access is acceptable for the intended review scope. <br>
Risk: Generated review reports may expose secrets, vulnerable code snippets, or other sensitive implementation details. <br>
Mitigation: Keep reports private until they have been reviewed and redacted for secrets or sensitive code. <br>
Risk: Team-sharing examples such as Slack, email, GitHub, cron, pre-commit, or API server workflows can broaden access to review output. <br>
Mitigation: Use those integrations only with explicit team approval and appropriate redaction and security controls. <br>


## Reference(s): <br>
- [Cuihua Code Reviewer ClawHub page](https://clawhub.ai/supermario11/cuihua-code-reviewer) <br>
- [Publisher profile](https://clawhub.ai/user/supermario11) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, terminal summaries, code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated reports may include sensitive code findings and should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
