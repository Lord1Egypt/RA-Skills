## Description:

Automates code testing by analyzing tasks, planning subtasks, executing tests, validating results, and returning reports, logs, and summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason513597](https://clawhub.ai/user/jason513597)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to add and run automated tests for a target code project, then review the resulting plan, test status, logs, and summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify accessible target directories while preparing tests.

Mitigation: Run it only against trusted projects in a disposable, isolated workspace.

Risk: The skill can install dependencies and execute project test code.

Mitigation: Keep sensitive credentials unavailable, review dependency files first, and avoid arbitrary filesystem targets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jason513597/skills/ai-autotester)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration]

**Output Format:** [JSON status output with generated pytest files and captured test logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update test and dependency files in the target project; captured stdout and stderr are summarized.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
