## Description:

FlowForge autonomously breaks coding tasks into spec, plan, code, and QA phases, executing heavy work via Claude Code with multi-account rate-limit rotation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[windseeker1111](https://clawhub.ai/user/windseeker1111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use FlowForge to turn feature, refactor, migration, investigation, or bug-fix tasks into a structured spec, plan, implementation, and QA workflow executed through Claude Code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify repositories and run generated commands autonomously.

Mitigation: Run it only in an isolated disposable environment and review planned changes before using results in a production repository.

Risk: Claude Code permission checks are disabled during the pipeline.

Mitigation: Use least-privilege workspaces and accounts, and inspect the skill scripts before installation or execution.

Risk: Untrusted GitHub issues, repositories, or sourced workspace configuration can influence command execution.

Mitigation: Avoid untrusted inputs and treat task descriptions, repository files, and workspace configuration as executable-risk material.

Risk: Copied Claude credential files are persisted for account rotation.

Mitigation: Treat saved credentials as bearer credentials, restrict file permissions, and avoid mounting personal credentials into the runtime environment.

## Reference(s):

- [FlowForge ClawHub Skill Page](https://clawhub.ai/windseeker1111/skills/flowforge)
- [README](README.md)
- [Spec Prompt](references/spec-prompt.md)
- [Planner Prompt](references/planner-prompt.md)
- [Coder Prompt](references/coder-prompt.md)
- [QA Prompt](references/qa-prompt.md)
- [Rubric Prompt](references/rubric-prompt.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, shell command output, and generated or modified repository files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a timestamped forge workspace containing clarifications, a specification, an implementation plan, a QA report, a session handoff note, and progress logs.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
