## Description:

Software Engineer for Projects is an instruction-only project engineering skill for codebase analysis, technical assessment, implementation planning, branch review, dev escalation handling, task manifests, and heartbeat queue checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[encryptshawn](https://clawhub.ai/user/encryptshawn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to coordinate software delivery across requirements review, architecture planning, implementation specifications, QA coverage planning, and escalation handling. It is intended for managed OpenClaw project workspaces where project files, queue files, and task-system permissions are controlled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent queue files can cause the skill to act on stale, malformed, or unauthorized task messages.

Mitigation: Install only in managed project workspaces and require operators to control write access to project folders and queue files.

Risk: The skill may update Asana or project state from queue-only messages where authority is ambiguous.

Mitigation: Clarify who may move tasks to Blocked and require confirmation before persistent file or task-system state is changed from queue-only input.

Risk: The skill depends on external git, Asana or ClickUp, and stack-specific skills for actions outside its instruction set.

Mitigation: Load only trusted dependency skills and keep their credentials scoped to the intended managed project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/encryptshawn/skills/dev-project-engineer)
- [OpenClaw Projects](https://clawhub.ai/encryptshawn/openclaw-projects)
- [Build Dev Team](https://clawhub.ai/encryptshawn/build-dev-team)
- [Engineering Design & Implementation Plan - Master Template](references/implementation_spec.md)
- [Code Analysis Reference](references/code_analysis.md)
- [Escalation Protocols](references/escalation_protocols.md)
- [Repo Operations Reference](references/repo_operations.md)
- [QA Coverage Plan Template](references/qa_spec.md)
- [Asana Task Guide - Task Manifest Format](references/asana_task_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, specifications, task manifests, review notes, and operational queue responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; relies on separately loaded git, Asana or ClickUp, and stack-specific skills for external actions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
