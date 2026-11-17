## Description:

Manages code task workflow by coordinating research, coding, review, security audit, testing, and commit stages with logging and planner updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[curbob](https://clawhub.ai/user/curbob)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to run a staged code-task workflow with specialized roles for implementation, review, security checks, testing, and release notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sub-agents may receive broader credentials than they need.

Mitigation: Use role-scoped, short-lived credentials instead of copying the main auth profile.

Risk: Plaintext board logging to a fixed internal endpoint may expose secrets or confidential implementation details.

Mitigation: Use a configurable HTTPS board endpoint and redact secrets and confidential details before logging.

## Reference(s):

- [Agent Pipeline skill page](https://clawhub.ai/curbob/skills/agent-pipeline)
- [Source skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown workflow guidance with inline commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces role-specific agent instructions, board update requests, branch naming guidance, and planner update guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
