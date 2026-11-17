## Description:

Guides agents through diagnosing and fixing confirmed bugs, distinguishing defects from feature changes, reproducing issues, applying minimal fixes, validating results, and writing reports for complex cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cping6](https://clawhub.ai/user/cping6)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to decide whether a reported issue is a true bug, reproduce and diagnose it, make targeted fixes, verify behavior with tests or tool-based checks, and document complex fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may lead an agent to edit code, run tests, use browser or database validation tools, and write reports inside a project.

Mitigation: Review tool permissions before use and avoid production database access unless that access is intentionally authorized.

Risk: A proposed bug fix can introduce regressions if the issue is not reproduced or verified.

Mitigation: Follow the skill's reproduction-first workflow and run focused tests or practical validation before considering the fix complete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cping6/skills/bugfix-workflow)
- [Bugfix report template](artifact/assets/bugfix-report-template.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, markdown, files]

**Output Format:** [Markdown guidance with optional code changes, shell commands, test results, and bug report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a dated bug-fix report for complex issues when the target project contains or needs a bug report directory.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
