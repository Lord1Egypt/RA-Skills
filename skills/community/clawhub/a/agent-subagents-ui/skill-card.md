## Description:

Add, extend, fix, or document the Subagents panel inside the OpenClaw Control UI Agents page.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to add or maintain the OpenClaw Control UI Subagents tab, including editable subagent model choices, fallback settings, thinking levels, and shared concurrency or depth limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated changes can persistently alter subagent model choices and concurrency or depth limits.

Mitigation: Review generated UI and configuration changes before saving them, and confirm they match the intended runtime model precedence.

Risk: The UI can become misleading if it invents unsupported per-agent settings or backend schema.

Mitigation: Keep the panel aligned with the referenced OpenClaw model-selection behavior and existing config form/save flow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maverick-software/skills/agent-subagents-ui)
- [File map](references/file-map.md)
- [Runtime precedence](references/runtime-precedence.md)
- [Implementation notes](references/implementation-notes.txt)
- [Subagents panel reference implementation](references/agents-panel-subagents.ts.txt)
- [Agents page wiring reference](references/agents.ts.txt)
- [App state reference](references/app.ts.txt)
- [App view state reference](references/app-view-state.ts.txt)
- [App render wiring reference](references/app-render.subagents.txt)
- [Focused UI tests reference](references/agents.test.ts.txt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with code and shell command suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce UI implementation changes that persist model choices and subagent concurrency or depth limits through the existing OpenClaw config save flow.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
