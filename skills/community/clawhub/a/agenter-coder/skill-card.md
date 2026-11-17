## Description:

Delegate coding tasks to a separate autonomous agent with AST validation, security scanning, automatic retry, four supported backends, budget limits, and structured JSON output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabriel-hurtado](https://clawhub.ai/user/gabriel-hurtado)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to delegate coding, bug fixing, refactoring, application creation, and test generation tasks to a separate autonomous coding process while receiving structured JSON results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The runtime delegates code edits and command execution to an external autonomous coding package.

Mitigation: Review and pin the agenter dependency before installation, keep sandboxing enabled, and inspect all diffs before trusting generated changes.

Risk: API credentials and model usage can create cost or access exposure.

Mitigation: Use least-privilege API keys and set finite cost, token, time, and iteration limits for each delegated task.

Risk: The skill can write broadly within the selected working directory if not constrained.

Mitigation: Restrict allowed write paths for the task and run the skill only in the intended workspace.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gabriel-hurtado/skills/agenter-coder)
- [Agenter SDK](https://github.com/Moonsong-Labs/agenter)
- [OpenClaw](https://openclaw.ai)
- [Backend Comparison](references/backends.md)

## Skill Output:

**Output Type(s):** [JSON, Code, Files, Shell commands, Configuration]

**Output Format:** [Structured JSON with status, summary, modified files, generated file contents, iteration counts, token use, cost, and duration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can stream NDJSON progress events when enabled; runtime should use finite budget limits and sandboxing.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
