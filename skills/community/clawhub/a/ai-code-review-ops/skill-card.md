## Description: <br>
AI Code Review guides agents through pull request review, code-quality checks, security inspection, performance analysis, and CI/CD status triage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review pull requests or local changes, assess code quality, security, performance, and maintainability, and summarize CI failures when GitHub CLI access is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can direct an agent using authenticated GitHub access to edit, commit, push, or apply dependency and audit fixes without a clear approval step. <br>
Mitigation: Require explicit user approval for the specific diff and command before edits, commits, pushes, dependency fixes, or audit fixes are executed. <br>
Risk: The skill may inspect pull requests, CI logs, or repository data through a user's GitHub login. <br>
Mitigation: Use the minimum required GitHub permissions and avoid exposing unrelated private repository, credential, or CI log data in review output. <br>


## Reference(s): <br>
- [AI Code Review ClawHub Release](https://clawhub.ai/terrycarter1985/ai-code-review-ops) <br>
- [Code Review Reference Guide](reference.md) <br>
- [Code Review Examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown review report with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CI/CD status, prioritized findings, remediation suggestions, and review notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
