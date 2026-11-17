## Description:

工作流编排中心 - 协调全流程，管理任务依赖和状态

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeyeshield](https://clawhub.ai/user/jeyeshield)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow authors use this skill to create, start, pause, resume, cancel, and monitor multi-step ad-production workflows. It coordinates dependent skill commands and includes a standard advertising production workflow template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow definitions can proxy commands to other skills with limited scoping.

Mitigation: Require explicit allowlists for callable skills and commands before production use.

Risk: Automatic event-triggered workflows can start advertising production and distribution actions without enough user control.

Mitigation: Require confirmation for distribution or paid-resource actions and restrict trusted workflow authors and event emitters.

Risk: Workflow arguments and event payloads may contain sensitive campaign or business data.

Mitigation: Validate workflow definitions and event payloads, and redact workflow arguments from logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jeyeshield/skills/ad-production-workflow-orchestrator)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON command responses and workflow status objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns workflow identifiers, status summaries, execution histories, statistics, and success or error messages.]

## Skill Version(s):

1.0.0 (source: server release, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
