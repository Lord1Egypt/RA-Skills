## Description: <br>
Supports pull request and code reviews by checking CI status, code quality, security, performance, tests, and maintainability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pull requests or changed code, inspect CI failures, and produce prioritized feedback on quality, security, tests, performance, and maintainability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may guide an agent to edit files, commit, and push changes while using the user's GitHub CLI context. <br>
Mitigation: Require explicit confirmation before file edits, commits, pushes, dependency installs, or execution of repository scripts. <br>
Risk: Reviewing untrusted repositories can expose the agent to unsafe scripts or project-specific commands. <br>
Mitigation: Use a sandbox for untrusted repositories and inspect commands before execution. <br>
Risk: The workflow is review-plus-remediation rather than read-only review. <br>
Mitigation: Treat generated fixes and CI remediation steps as proposals until a human reviewer approves them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/code-review-terry) <br>
- [Code Review Reference Guide](artifact/reference.md) <br>
- [Code Review Examples](artifact/examples.md) <br>
- [The Twelve-Factor App: Config](https://12factor.net/config) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with review sections, inline code snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CI/CD status summaries, prioritized findings, concrete remediation suggestions, and local verification commands.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
