## Description:

Captures learnings, errors, corrections, feature requests, and recurring patterns so agents can log them to `.learnings/` and promote durable guidance into project or workspace memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blockcloud](https://clawhub.ai/user/blockcloud)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to capture corrections, command failures, missing capabilities, and useful discoveries in structured Markdown logs. It also guides review and promotion of broadly useful learnings into agent memory or reusable skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning notes and promoted memory files can preserve sensitive or incorrect context across sessions.

Mitigation: Keep learning logs project-local where possible, redact secrets and private context, and require review before promoting entries into agent instruction files.

Risk: Automatic hooks and broad error logging can capture raw command output or transcript details that were not intended for reuse.

Mitigation: Use opt-in project-level hooks, avoid user-level or global hook activation, and sanitize command output before it is written or shared.

Risk: Cross-session sharing can spread unreviewed guidance beyond the original task context.

Mitigation: Share only concise, reviewed learnings and avoid sending transcript content, credentials, private user context, or unresolved assumptions.

## Reference(s):

- [OpenClaw Integration](references/openclaw-integration.md)
- [Hook Setup Guide](references/hooks-setup.md)
- [Entry Examples](references/examples.md)
- [Agent Skills Specification](https://agentskills.io/specification)
- [ClawHub Skill Page](https://clawhub.ai/blockcloud/skills/cpppselfimprovingagent123123)
- [Publisher Profile](https://clawhub.ai/user/blockcloud)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured learning entries, setup snippets, hook reminders, and skill scaffolding guidance.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
