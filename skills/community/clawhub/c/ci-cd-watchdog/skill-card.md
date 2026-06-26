## Description: <br>
CI/CD流水线智能运维助手，自动解析构建日志、定位根因、生成修复方案与回滚指令、输出事后复盘报告 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
DevOps engineers and development teams use this skill to analyze CI/CD failure logs, identify likely root causes, and produce repair, rollback, and post-mortem guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CI logs may contain secrets or internal infrastructure details. <br>
Mitigation: Redact tokens, passwords, private IPs, and other sensitive values before providing logs to the skill. <br>
Risk: Generated repair or rollback commands may not match the target repository, environment, or approval process. <br>
Mitigation: Review commands as suggestions and validate paths, commits, environment assumptions, and approvals before use, preferably with staging or dry-run execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/boboy-j/ci-cd-watchdog) <br>
- [Python dependency resolution documentation](https://pip.pypa.io/en/latest/topics/dependency-resolution/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown diagnostic report with tables, checklists, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a pipeline_log input and can optionally use ci_platform and repo_context.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
