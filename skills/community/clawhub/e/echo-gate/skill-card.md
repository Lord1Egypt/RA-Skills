## Description:

Use Echo Gate when registering, exposing, calling, securing, auditing, or operating local-first agent-callable tools through the BuiltByEcho gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[builtbyecho](https://clawhub.ai/user/builtbyecho)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to register and operate local-first agent-callable tools through Echo Gate, including API keys, gateway calls, receipts, approvals, secret handling, and spend limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A global npm install without a pinned reviewed version could install code the reviewer has not assessed.

Mitigation: Install only from a trusted BuiltByEcho package source and prefer a pinned, reviewed @builtbyecho/echo-gate version.

Risk: Gateway administration and tool calls involve sensitive tokens such as ECHO_GATE_ADMIN_TOKEN and ECHO_GATE_KEY.

Mitigation: Keep tokens out of chat, documentation, commits, and public issue comments; use local environment variables and revoke keys that are no longer needed.

## Reference(s):

- [Echo Gate ClawHub Skill Page](https://clawhub.ai/builtbyecho/skills/echo-gate)
- [Echo Gate Project Repository](https://github.com/BuiltByEcho/echo-gate)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, environment variables, HTTP endpoints, and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on local-first gateway operations; may include commands that install or call the @builtbyecho/echo-gate package.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
