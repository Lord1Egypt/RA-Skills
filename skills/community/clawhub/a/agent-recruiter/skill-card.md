## Description:

Agent Recruiter helps create, configure, and manage OpenClaw agents, including agent workspaces, identity files, Feishu group bindings, and gateway updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junchen19](https://clawhub.ai/user/junchen19)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to create or optimize agents, populate SOUL and IDENTITY templates, configure Feishu group routing, and prepare OpenClaw workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recruitment script can copy another agent's authentication profile into a newly created agent.

Mitigation: Do not copy auth profiles by default; require explicit user approval and review credentials before installation or execution.

Risk: The skill can change persistent OpenClaw routing and bind agents to Feishu groups.

Mitigation: Validate agent IDs and group IDs, use user-approved routing values, and review openclaw.json changes before restarting the gateway.

Risk: Generated maintenance agents may receive broad system powers without enough scoping.

Mitigation: Limit new agents to report-only behavior unless a user explicitly approves each state-changing action.

Risk: Inline JavaScript interpolation in the setup script can make configuration edits unsafe when inputs are not tightly controlled.

Mitigation: Remove inline interpolation or strictly sanitize shell and JavaScript inputs before running the script.

## Reference(s):

- [Agent Recruiter on ClawHub](https://clawhub.ai/junchen19/skills/agent-recruiter)
- [agency-agents template reference](https://github.com/msitarzewski/agency-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash, JSON, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce OpenClaw agent workspace files and persistent routing configuration when its shell script is executed.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
