## Description:

Spawn sub-agents for independent work that needs file edits, builds, or long-running tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dodge1218](https://clawhub.ai/user/dodge1218)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to delegate substantial independent tasks to a bounded sub-agent when file edits, builds, or long-running execution would be too heavy for inline work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sub-agent delegation can produce incorrect or incomplete changes, especially when file edits or builds are involved.

Mitigation: Review sub-agent outputs before relying on them and verify that the expected output file, URL, or test result exists.

Risk: Long-running delegated tasks can consume agent time or model capacity without reaching a useful result.

Mitigation: Use one sub-agent at a time, require clear exit criteria, and stop after two failed attempts as directed by the workflow.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown workflow guidance with a reusable task prompt template]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Directs use of one sub-agent at a time, requires explicit role, context, and exit criteria, and asks the operator to verify produced artifacts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
