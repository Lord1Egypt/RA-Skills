## Description:

SENTINEL/CORD governance engine for mandatory pre-flight checks of agent tool calls, external input scanning, blocked-action review, CORD audit log status, and intent lock setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zanderone1980](https://clawhub.ai/user/zanderone1980)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route significant tool calls and external inputs through CORD risk checks, inspect blocked decisions, review audit status, and set session intent locks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to mediate broad agent actions and external inputs through cord_engine.

Mitigation: Review before installing and use it only when you trust the exact cord_engine package or configured installation path.

Risk: Commands and input summaries may be evaluated and logged by the CORD workflow.

Mitigation: Confirm where intent locks and audit logs are stored before use, and avoid passing secrets or unnecessary sensitive content into evaluations.

Risk: The referenced Python engine is not bundled with the skill artifact and has weak dependency scoping.

Mitigation: Pin and verify the cord_engine source used by the agent before enabling the skill in a production workspace.

## Reference(s):

- [CORD Python API Reference](references/cord-api.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with bash and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a trusted cord_engine installation path or package.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
