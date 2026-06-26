## Description: <br>
Validate git commit messages against Conventional Commits spec and configurable rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to lint commit messages, enforce Conventional Commits rules, configure commit-message policies, and generate CI or hook-friendly reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strict commit-message rules can block commits or CI builds when adopted without repository-specific review. <br>
Mitigation: Review the lint configuration before enforcing it in CI or a git hook, and test it against representative commit history. <br>
Risk: The linter reads local commit messages from git, stdin, or files, which may contain sensitive project information. <br>
Mitigation: Use it only in repositories whose commit history and commit-message files are appropriate to lint locally. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/charlie-morrison/commit-message-linter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; the bundled script can emit text, JSON, or Markdown reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Exit codes indicate pass, lint failure, or git/system error.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
