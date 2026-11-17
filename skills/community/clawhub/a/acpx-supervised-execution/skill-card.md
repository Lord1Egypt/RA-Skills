## Description:

Use when a coding, debugging, or research task should run inside one long-lived ACPX session while a separate supervisor keeps checking real engineering progress until the work is accepted complete or explicitly failed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[programcaicai](https://clawhub.ai/user/programcaicai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to run a single long-lived ACPX execution session with a separate low-frequency supervisor that checks concrete engineering evidence, sends corrections to the same session, and reports accepted or failed completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The supervised workflow can keep a long-running task active without useful progress if the task brief, evidence paths, acceptance criteria, or failure conditions are vague.

Mitigation: Before using the skill, define the task brief, evidence paths, acceptance and failure conditions, and require the supervisor to close the main session when the task is accepted or failed.

Risk: Supervisor corrections may steer the execution session based on incomplete or misleading progress evidence.

Mitigation: Review real engineering evidence such as diffs, tests, logs, reports, generated artifacts, commits, or blocker notes before accepting progress or sending corrections.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with prompt templates, checklists, and report structures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces task briefs, progress reports, supervisor reviews, correction prompts, and final completion or failure reports.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
