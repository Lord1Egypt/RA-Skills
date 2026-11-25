## Description:

Triage long-running red CI: attribute failures to commits, locate the failing step per job, distinguish a broken gate from a failing one, and fix environment-dependency assertions. Infrastructure failures are not code changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyunlai](https://clawhub.ai/user/zuoyunlai)

### License/Terms of Use:

MIT

## Use Case:

Developers and CI maintainers use this skill to trace persistent CI failures to the responsible commit and job step, distinguish broken gates from actual code failures, and address environment-dependent tests. It also guides safe handling of infrastructure failures and post-push verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions include cleanup of a fixed temporary directory.

Mitigation: Check the exact path and its contents before running cleanup commands, and preserve any data needed by other work.

Risk: The workflow includes repository and publishing commands that can change or publish project state.

Mitigation: Review the proposed changes and destination remote, then confirm that publishing is intended before pushing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zuoyunlai/skills/ci-long-red-triage)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnosis and remediation guidance depends on the repository, CI runs, and job logs under review.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
