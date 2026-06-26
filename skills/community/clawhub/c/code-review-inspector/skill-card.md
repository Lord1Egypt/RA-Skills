## Description: <br>
Automated code review checking for bugs, security issues, best practices, performance problems, and code style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[michaelatamuk](https://clawhub.ai/user/michaelatamuk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review code changes, diffs, or selected files before commits and pull requests. It helps identify bugs, security issues, performance problems, best-practice gaps, style concerns, missing tests, and documentation issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect repository files or diffs that contain proprietary code, credentials, or other sensitive material. <br>
Mitigation: Use it only on repositories and diffs the agent is allowed to inspect, and do not provide unrelated private files, payment access, or credentials. <br>
Risk: Automated review findings can be incomplete, incorrect, or missing project-specific context. <br>
Mitigation: Treat findings as suggestions and verify important issues with tests and human review before making release or merge decisions. <br>


## Reference(s): <br>
- [Code Review Checklist](CODE_REVIEW_CHECKLIST.md) <br>
- [Code Review Inspector ClawHub page](https://clawhub.ai/michaelatamuk/code-review-inspector) <br>
- [OWASP Top 10](https://owasp.org/www-project-top-ten/) <br>
- [Google Engineering Practices: Code Review](https://google.github.io/eng-practices/review/) <br>
- [Refactoring Catalog](https://refactoring.com/catalog/) <br>
- [OWASP Code Review Guide](https://owasp.org/www-project-code-review-guide/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown review report with prioritized findings, explanations, and suggested fixes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings are suggestions to verify with tests and human review.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
