## Description: <br>
Supports code review by checking pull requests, code quality, security issues, performance concerns, maintainability, tests, and CI/CD status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review pull requests or local code changes, summarize CI failures, identify quality and security concerns, and propose practical fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move from review into changing code, updating dependencies, committing, pushing, or fixing CI with the user's GitHub account. <br>
Mitigation: Require explicit user confirmation and a shown diff before any file modification, commit, push, dependency update, or CI-fix action. <br>
Risk: The skill may inspect repositories, pull requests, CI logs, and GitHub account state. <br>
Mitigation: Use it only on repositories the user is authorized to inspect, verify the active GitHub account before running GitHub CLI commands, and avoid exposing secrets from logs or local configuration. <br>
Risk: The skill may rely on local agent guidance from ~/.claude/CLAUDE.md. <br>
Mitigation: Review local guidance before use and override any repository-specific or user-specific instructions that conflict with the intended review scope. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/ai-code-review-skill) <br>
- [Detailed Review Criteria](artifact/reference.md) <br>
- [Review Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown with issue summaries, review comments, code snippets, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, commits, pushes, dependency updates, or CI fixes when the user grants permission.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
