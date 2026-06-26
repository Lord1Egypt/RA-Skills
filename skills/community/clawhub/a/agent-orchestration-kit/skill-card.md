## Description: <br>
Set up and manage multi-agent task orchestration on OpenClaw with async dispatch, leader coordination, real-time tracking, and approval workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kuan0808](https://clawhub.ai/user/kuan0808) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to scaffold and operate a leader-led multi-agent team. It helps coordinate asynchronous task dispatch, task-file tracking, callback handling, quality review, and owner approval before external actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup changes OpenClaw-wide agent orchestration settings, including session visibility, internal hooks, heartbeat, agent-to-agent communication, and trusted exec paths. <br>
Mitigation: Run the documented dry-run first, review each proposed configuration change, proceed only after explicit confirmation, and keep the generated openclaw.json backup for rollback. <br>
Risk: Delegated agents may prepare outputs that affect external systems, such as publishing, deploying, pushing, sending, or deleting. <br>
Mitigation: Use the built-in approval workflow so external actions remain pending until the owner explicitly approves them. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kuan0808/agent-orchestration-kit) <br>
- [Architecture](references/architecture.md) <br>
- [Approval Workflow](references/approval-workflow.md) <br>
- [Brief Templates](references/brief-templates.md) <br>
- [Communication Signals](references/signals.md) <br>
- [Agency Agents](https://github.com/msitarzewski/agency-agents) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with shell commands, configuration changes, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenClaw workspace templates, shared operations files, task-tracking conventions, and configuration patch guidance.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
