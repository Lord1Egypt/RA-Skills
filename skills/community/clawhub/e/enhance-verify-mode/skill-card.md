## Description: <br>
验证模式 — 检查工作成果、运行测试、验证假设。借鉴 Claude Code 的 Verification Agent。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers use this skill to verify completed code changes or hypotheses by checking logic, edge cases, tests, builds, and security-sensitive behavior, then producing an evidence-backed verification report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Verification may involve running tests, builds, linters, or other repository commands in sensitive workspaces. <br>
Mitigation: Review commands before approval and run them with the least privileges needed for the repository. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jobzhao15/enhance-verify-mode) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown verification report with checklist items, findings, severity, and conclusion] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include test, build, or lint command recommendations and evidence from command results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
