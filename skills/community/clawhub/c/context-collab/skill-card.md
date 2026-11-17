## Description:

Multi-agent collaboration protocol engine for OpenClaw that creates shared group spaces, can auto-inject SPACE.md, TEAM.md, and TASK.md into agent conversations, and provides tools for shared files, tasks, members, and annotations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luojingwei123](https://clawhub.ai/user/luojingwei123)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams using OpenClaw use this skill to coordinate multi-agent work through a shared Context space with shared protocol files, task state, team membership, annotations, and file operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared remote files can influence linked group conversations through automatic prompt injection.

Mitigation: Install only for trusted teams and servers, disable autoInject unless this behavior is intended, and avoid storing secrets or private work products in Context spaces.

Risk: Shared space data can be written or deleted, including irreversible space deletion behavior.

Mitigation: Use a Context server with authentication, per-space authorization, audit logs, and deletion recovery before relying on the skill for important collaboration data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luojingwei123/skills/context-collab)
- [Publisher profile](https://clawhub.ai/user/luojingwei123)
- [Context web UI](https://context-server-mj6f.onrender.com/s)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Text and JSON tool responses, with shared Markdown files and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can auto-inject shared protocol content into group prompts when autoInject is enabled.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
