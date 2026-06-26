## Description: <br>
Automated code review, quality gates, and PR analysis. Integrates with GitHub, GitLab, Bitbucket. Enforce style guides, detect bugs, security vulnerabilities, performance issues. Auto-approve safe PRs, flag dangerous changes. Save developers 5+ hours/week on manual reviews. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Fuczy](https://clawhub.ai/user/Fuczy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review pull requests, enforce coding standards, detect bugs and security issues, and generate review feedback across GitHub, GitLab, and Bitbucket workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can auto-approve or block pull requests. <br>
Mitigation: Keep auto-approval disabled unless limited to clearly low-risk changes, and preserve human review for protected branches and security-sensitive files. <br>
Risk: Repository and pull request metadata may be shared through Slack notifications. <br>
Mitigation: Treat notifications as external sharing and configure channels, scopes, and recipients accordingly. <br>
Risk: Repository integrations may receive broad permissions if installed without scoping. <br>
Mitigation: Use least-privilege bot permissions and install only on selected repositories. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Fuczy/clawd-code-reviewer) <br>
- [Skill homepage](https://clawhub.com/skills/code-reviewer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with YAML, Bash, Python, and CI configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include PR review comments, pass/warn/fail summaries, suggested fixes, rule configuration, and CI setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
