## Description: <br>
Monitor GitHub Actions CI pipelines for failures and automatically fix common issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielgrobelny](https://clawhub.ai/user/danielgrobelny) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to monitor GitHub Actions failures, inspect logs, apply common CI fixes, and report issues that require human intervention. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive recurring automated repository changes and pushes using the user's GitHub access. <br>
Mitigation: Set CI_REPOS explicitly, use a least-privilege GitHub token, run the skill on demand before enabling cron, and require human approval or pull request review before any commit or push. <br>
Risk: The skill reads GitHub Actions logs, which may expose sensitive build details. <br>
Mitigation: Install only where access to GitHub Actions logs is acceptable, and scope credentials to the repositories that need CI monitoring. <br>


## Reference(s): <br>
- [CI Failure Fix Patterns](references/fix-patterns.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/danielgrobelny/ci-failure-fixer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and diagnosis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated GitHub CLI and may read GitHub Actions logs or propose repository changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
