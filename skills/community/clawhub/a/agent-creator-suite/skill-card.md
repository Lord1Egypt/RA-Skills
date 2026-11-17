## Description:

Build high-performing OpenClaw agents end-to-end by designing a persona, operating rules, safety posture, and required OpenClaw workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryan-wuxl](https://clawhub.ai/user/ryan-wuxl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced agent users use this skill to create or revise OpenClaw agent workspaces with tailored identity, behavior, memory, heartbeat, and safety files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated workspace memory and heartbeat files can create durable agent behavior that persists across sessions.

Mitigation: Review generated MEMORY.md and HEARTBEAT.md content before use, and enable heartbeat behavior only after the generated agent rules are trusted.

Risk: Workspace files may accidentally capture sensitive user, credential, or session details.

Mitigation: Keep credentials and private session transcripts out of generated workspace files, and review memory content before committing or sharing the workspace.

## Reference(s):

- [Project homepage](https://github.com/ryan-wuxl/agent-creator-suite)
- [OpenClaw workspace reference](references/openclaw-workspace.md)
- [OpenClaw agent file templates](references/templates.md)
- [Agent architecture patterns](references/architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and OpenClaw workspace file content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or revise IDENTITY.md, SOUL.md, AGENTS.md, USER.md, HEARTBEAT.md, optional MEMORY.md, daily memory notes, and acceptance-test prompts.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
