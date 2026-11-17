## Description:

Orchestrate Cursor Agent CLI for coding tasks with concurrency control, timeout recovery, and multi-task coordination.

This skill is ready for commercial/non-commercial use.

## Publisher:

[slk1061569042-lab](https://clawhub.ai/user/slk1061569042-lab)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to delegate focused coding, analysis, and review tasks to Cursor Agent CLI while coordinating concurrency, timeouts, retries, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delegated Cursor Agent execution can modify repositories, run project commands, and create commits when auto-approval patterns are used.

Mitigation: Prefer plan and review flows, avoid auto-approved execution on untrusted repositories, and manually review verification commands and commits.

Risk: Broad process cleanup commands can stop unrelated Cursor sessions.

Mitigation: Use targeted session cleanup first and reserve global process termination for deliberate recovery cases.

## Reference(s):

- [Models and Parameters Reference](references/models-and-params.md)
- [Cursor Dispatch on ClawHub](https://clawhub.ai/slk1061569042-lab/skills/cursor-dispatch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and command templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include process orchestration steps, timeout values, retry guidance, and verification commands.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
