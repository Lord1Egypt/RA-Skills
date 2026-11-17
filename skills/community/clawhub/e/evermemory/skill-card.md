## Description:

EverMemory helps OpenClaw and ClawHub agents store, recall, inspect, govern, export, import, and explain persistent memory, preferences, profiles, rules, and archived context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiehao321](https://clawhub.ai/user/jiehao321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use EverMemory to give an agent durable continuity across sessions, including remembered facts, decisions, preferences, user profiles, behavior rules, briefings, backup and restore workflows, and explanations for memory actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain sensitive facts, preferences, project context, profiles, and behavior rules longer than a user expects.

Mitigation: Install only when durable memory is intended, avoid saving secrets unless persistence is deliberate, and use inspect, export, archive, and restore review workflows to manage retained data.

Risk: Imports and restores can reintroduce outdated, incorrect, or unwanted memory.

Mitigation: Review imported or archived items before applying changes, and restore only the specific records the user approves.

## Reference(s):

- [EverMemory on ClawHub](https://clawhub.ai/jiehao321/skills/evermemory)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown or text guidance with JSON examples and configuration names]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agent use of persistent-memory tools; may reference memory exports, imports, restore reviews, status reports, profiles, rules, and briefings.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
