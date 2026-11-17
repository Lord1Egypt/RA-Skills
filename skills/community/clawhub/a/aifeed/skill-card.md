## Description:

Verify signed AIFeed declarations and publish signed AIFeed origins (permissions, feeds, manifests).

This skill is ready for commercial/non-commercial use.

## Publisher:

[denyn1](https://clawhub.ai/user/denyn1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and publishers use this skill to verify signed AIFeed permission declarations before fetching content and to publish signed AIFeed origins with manifests, DNS anchors, revocation checks, and adapter guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Referenced external CLI, SDK, studio, or MCP server packages could execute code outside the reviewed skill artifact.

Mitigation: Source those packages from a trusted location, review them before use, and run commands only in the intended project directory.

Risk: Publisher key generation creates private keys that could be exposed through commits or logs.

Mitigation: Keep generated private keys local, maintain restrictive file permissions, and exclude key material from commits and logs.

## Reference(s):

- [AIFeed on ClawHub](https://clawhub.ai/denyn1/skills/aifeed)
- [Publisher profile](https://clawhub.ai/user/denyn1)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes verify-first usage guidance, publisher setup commands, MCP server invocation, and conformance gate notes.]

## Skill Version(s):

1.0.0-draft.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
