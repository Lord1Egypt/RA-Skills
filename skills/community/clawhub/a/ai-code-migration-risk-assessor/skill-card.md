## Description: <br>
Analyzes code-change risk, assesses impact scope, and generates practical refactoring plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review pull requests, repository changes, large refactors, external code migrations, and API upgrades for risk level, affected modules, and a step-by-step remediation plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may inspect repository diffs, commit history, code search results, and audit-style operational data. <br>
Mitigation: Run it only on repositories and logs the reviewing agent is authorized to access, and avoid exposing secrets in diffs or prompts. <br>
Risk: GitHub or related access tokens could grant more repository access than the assessment requires. <br>
Mitigation: Use least-privilege tokens and limit token scope to the repositories and read operations needed for the review. <br>
Risk: Generated risk ratings and refactoring plans can be incomplete or incorrect for complex production changes. <br>
Mitigation: Treat results as review guidance and have qualified engineers validate high-risk findings, migration steps, and test coverage before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zlszhonglongshen/ai-code-migration-risk-assessor) <br>
- [README.md](artifact/README.md) <br>
- [workflow.json](artifact/workflow.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown risk report with risk levels, affected-module lists, refactoring steps, and action-plan guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use repository diffs, commit history, code search results, and dependent analysis skills when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
