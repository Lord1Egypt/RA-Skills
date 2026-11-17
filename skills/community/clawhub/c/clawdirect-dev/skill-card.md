## Description:

Build agent-facing web experiences with ATXP-based authentication, following the ClawDirect pattern.

This skill is ready for commercial/non-commercial use.

## Publisher:

[napoleond](https://clawhub.ai/user/napoleond)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build agent-facing web applications that support browser interaction, MCP tools, ATXP authentication, optional payments, and cookie-based access patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented browser authentication pattern can expose reusable session credentials when cookie values are passed through URLs.

Mitigation: Use one-time, short-lived bootstrap tokens or direct cookie-setting support instead of reusable URL-carried cookies.

Risk: The template stores server-side sessions without clear expiration or revocation behavior.

Mitigation: Add explicit session expiration and revocation before adapting the pattern for production.

Risk: Unpinned dependency and CLI versions can change behavior across installs.

Mitigation: Pin dependency and CLI versions before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/napoleond/skills/clawdirect-dev)
- [ClawDirect Reference Implementation](https://github.com/napoleond/clawdirect)
- [ATXP CLI Documentation](https://skills.sh/atxp-dev/cli/atxp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code, shell command, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces templates and implementation guidance for Node.js, Express, SQLite, MCP, and ATXP-based web apps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
