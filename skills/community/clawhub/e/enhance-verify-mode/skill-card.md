## Description:

验证模式 — 检查工作成果、运行测试、验证假设。借鉴 Claude Code 的 Verification Agent。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jobzhao15](https://clawhub.ai/user/jobzhao15)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to verify completed code changes, inspect assumptions, run relevant tests or checks, and produce a concise verification report with findings and evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification may involve running tests, build checks, linters, or formatters that are expensive or may modify files.

Mitigation: Review or confirm commands first in repositories where test runs are costly or formatter edits are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jobzhao15/skills/enhance-verify-mode)
- [Project homepage](https://github.com/jobzhao15/openclaw-enhance)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown verification report with checklists, test results, findings, and conclusions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or run repository tests, build checks, linters, or formatters depending on the verification target.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
