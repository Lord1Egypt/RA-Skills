## Description:

Guides the design of short-lived authorization codes and a local credential broker so agents can receive revocable, scoped access without placing vault secrets in model context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT for Python code only; documentation and theoretical text all rights reserved

## Use Case:

Developers and engineers use this skill to plan scoped, time-limited access for AI agents and local applications, with credential retrieval, audit trails, and revocation handled by a local broker rather than the model context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A dashboard PIN in a URL can be exposed through URL handling or printed links.

Mitigation: Remove query-string PIN authentication and avoid printing secret-bearing URLs before using real vault secrets.

Risk: A local caller with the PIN can retrieve passwords from the broker.

Mitigation: Review and restrict local caller access; do not run the broker with real vault secrets until its authentication and secret-handling risks are addressed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/authz-code-design)
- [Local credential broker architecture](references/broker-arch.svg)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Text or Markdown, with code and configuration examples where useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can follow the user's language.]

## Skill Version(s):

1.1.3 (source: ClawHub release; bundled files say 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
