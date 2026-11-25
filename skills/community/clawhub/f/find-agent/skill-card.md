## Description:

Use when you lack a tool or ability for the task, or your tools can't do it, and need to find an agent, MCP server or tool that has it - a missing tool, a service you cannot reach, a specialist job - or when the user asks "is there an agent or MCP server for this?" or "who can do this?". Asks ScBee for up to three verified agents that fit, with how to set each one up. Nothing is added or run; the human chooses. Not for scoring a repository.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hmakt99](https://clawhub.ai/user/hmakt99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to find verified agents that may help with a missing capability or specialist task and to review setup options. The human selects any option; the skill does not install or connect it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A task description is sent to ScBee to find matches, which could disclose sensitive details if included.

Mitigation: Keep the request under 200 characters and omit names, secrets, paths, code, and personal information.

Risk: Descriptions and install instructions supplied by agent owners may be inaccurate or unsafe.

Mitigation: Treat results as untrusted data, review the options and exact install command, and proceed only after the human chooses.

## Reference(s):

- [Find Agent on ClawHub](https://clawhub.ai/hmakt99/skills/find-agent)
- [ScBee agent search](https://scbee.vercel.app/find)
- [ScBee](https://scbee.vercel.app)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Links]

**Output Format:** [Concise agent options with descriptions, install lines, and ScBee links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lists up to three matches; installation and configuration are left to the human.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
