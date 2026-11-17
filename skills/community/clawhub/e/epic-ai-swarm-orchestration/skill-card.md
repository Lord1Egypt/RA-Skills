## Description:

Production playbook and portable runtime for parallel AI coding swarms using Codex, Gemini, DeepSeek, and optional Claude.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkbag](https://clawhub.ai/user/linkbag)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan, spawn, monitor, review, and integrate parallel coding agents through a portable OpenClaw swarm runtime. It is intended for multi-agent coding work, runtime packaging, duty-table model rotation, fallback handling, and swarm health diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The swarm runtime gives autonomous agents broad execution, network, git, and persistence authority.

Mitigation: Install and run it only in an isolated workspace or disposable account with provider credentials scoped to the swarm.

Risk: Unsafe defaults may affect sandbox behavior, dependency installation, task input handling, temporary-file handling, and review failure handling.

Mitigation: Review and harden spawn-agent.sh and related watcher scripts before using the runtime on important projects.

Risk: External model providers, git pushes, background watchers, and configured notification targets may receive project metadata.

Mitigation: Avoid private or sensitive repositories unless that exposure is acceptable and notification targets are configured deliberately.

## Reference(s):

- [Workflow details](references/workflow.md)
- [Spawn command syntax](references/tools.md)
- [Duty table and fallback](references/duty-table.md)
- [End-of-run report template](references/eor-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON task examples, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include agent task plans, runtime command sequences, status checks, and integration guidance for the local swarm installation.]

## Skill Version(s):

3.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
