## Description:

Helps agents create and manage monthly OKRs, weekly task breakdowns, and weekly review reports with two-level approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-team operators use this skill to define monthly objectives and key results for agents, split them into weekly tasks, and prepare weekly progress reports for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled OKR validator can execute code when run on directories containing crafted OKR filenames.

Mitigation: Review before installing and do not run scripts/validate-okr.sh on directories with untrusted filenames until file paths are passed as arguments instead of interpolated into Python source.

Risk: The workflow can write weekly report updates to docs/agent-okr files.

Mitigation: Require explicit user approval before weekly report writes and keep changes limited to the intended docs/agent-okr path.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown guidance with YAML examples and shell command references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in YAML OKR files and weekly report content under docs/agent-okr when an agent follows the workflow.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
