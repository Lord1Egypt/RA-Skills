## Description:

Persistent cognitive memory for AI agents -- query, record, review, and consolidate knowledge across sessions with spreading activation, FSRS scheduling, and NLI contradiction detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fozikio](https://clawhub.ai/user/fozikio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to connect agents to a local persistent-memory MCP service for querying prior knowledge, recording facts and questions, tracking work across sessions, and producing memory-grounded reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and relies on a changing third-party local service package.

Mitigation: Review the @fozikio/cortex-engine package before installation and prefer a reviewed pinned version or local locked install when possible.

Risk: Observations, beliefs, operational notes, and consolidations persist across agent sessions.

Mitigation: Avoid storing secrets unless intentional, and periodically review or prune persisted memory contents.

Risk: The local memory service may access local resources while running.

Mitigation: Run the service with the least local access practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fozikio/skills/cortex-engine)
- [@fozikio/cortex-engine npm package](https://www.npmjs.com/package/@fozikio/cortex-engine)
- [Cortex Engine project](https://github.com/Fozikio/cortex-engine)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline tool examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides use of a local MCP memory service and may produce structured review notes grounded in stored memory.]

## Skill Version(s):

1.1.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
