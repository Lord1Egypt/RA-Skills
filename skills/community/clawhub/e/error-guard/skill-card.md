## Description:

System safety and control-plane skill that helps OpenClaw agents inspect task state, cancel long-running work, flush message queues, and recover from deadlocks or freezes without restarting the container.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amar1432](https://clawhub.ai/user/amar1432)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to add control-plane recovery primitives for long-running OpenClaw tasks, sub-agents, benchmark workers, and background monitors. It is intended for advanced users who need non-LLM status, flush, cancellation, watchdog, and recovery controls when work can block or hang.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The emergency recovery path can kill visible process sessions without ownership checks or confirmation.

Mitigation: Limit /flush and /recover to skill-owned sessions, require explicit operator authorization or confirmation, preserve accurate success/failure results, and document the risk of losing unrelated in-flight work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amar1432/skills/error-guard)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command names and JSON-like status or recovery results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands are designed to be non-LLM control-plane actions that report status, cancel tracked work, clear queues, or initiate recovery.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
