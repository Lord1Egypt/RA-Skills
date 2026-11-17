## Description:

FIS Architecture helps CyberMao and worker agents coordinate multi-agent workflows with JSON tickets, A2A notifications, and Discord forum threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[muselinn](https://clawhub.ai/user/muselinn)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to delegate coding, research, and writing tasks between CyberMao and specialized worker agents while tracking status across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details may be shared through Discord threads and #daily-chat.

Mitigation: Restrict Discord bot permissions and channel access, and avoid posting sensitive content to public threads or #daily-chat.

Risk: Ticket state is persisted locally across sessions.

Mitigation: Keep FIS_HUB_PATH confined to a dedicated directory and avoid storing sensitive task details in ticket files.

Risk: Generated sessions_* commands can send task content to other agents or spawn background work.

Mitigation: Review generated sessions_* commands before executing them.

Risk: The server security summary flags unsafe ticket-file handling.

Mitigation: Use trusted ticket identifiers and a restricted FIS_HUB_PATH, and review local ticket files before acting on them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/muselinn/skills/fis-architecture)
- [Artifact Homepage](https://github.com/linn/fis-architecture)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON request examples, and generated coordination messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ticket lifecycle commands, delegation templates, A2A notification text, and Discord thread request examples.]

## Skill Version(s):

3.3.1 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
