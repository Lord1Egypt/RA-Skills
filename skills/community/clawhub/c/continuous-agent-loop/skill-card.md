## Description: <br>
Provides canonical patterns for autonomous agent loops with quality gates, evaluations, session persistence, and recovery controls across sequential, RFC, CI/PR, and exploratory workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djc00p](https://clawhub.ai/user/djc00p) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to structure autonomous coding or analysis loops, define quality gates, run repository harness audits, and recover from loop churn or failing iterations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit helper could be run against the wrong repository or directory. <br>
Mitigation: Set AUDIT_ROOT or pass --root to the intended project before running the audit. <br>
Risk: Autonomous loop workflows could proceed into push, pull request, or merge actions without adequate human review. <br>
Mitigation: Keep explicit human approval around workflows that push, open pull requests, or merge code. <br>
Risk: Poorly bounded loops can churn, retry the same root cause, or drift in cost. <br>
Mitigation: Define pass/fail criteria before each iteration, cap budgets, freeze on repeated failures, and reduce scope to the failing unit. <br>


## Reference(s): <br>
- [Harness Audit Command](references/harness-audit.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/djc00p/continuous-agent-loop) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON audit output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The harness audit helper can emit text or JSON scorecards for the selected scope.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
