## Description:

Server-side runtime patterns for CopilotKit runtime endpoints, remote agent configuration, middleware, and runtime security.

This skill is ready for commercial/non-commercial use.

## Publisher:

[generaljerel](https://clawhub.ai/user/generaljerel)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill when setting up or maintaining CopilotKit server-side runtimes, including Express, Hono, and Next.js endpoints, remote agent registration, middleware, security controls, and streaming behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security examples may be under-scoped for production authentication and rate limiting.

Mitigation: Review and harden the examples before use, deriving identity from verified server-side session or JWT state and rate limiting by authenticated user or API key.

Risk: Long-lived tokens or sensitive request data could be exposed through browser properties or logs.

Mitigation: Avoid exposing long-lived browser tokens, minimize request logging, and redact sensitive request and response fields.

Risk: Users may copy draft guidance into production without adapting it to their deployment.

Mitigation: Treat the skill as draft guidance, then perform a security review of authentication, CORS, rate limits, and streaming configuration before deployment.

## Reference(s):

- [CopilotKit Documentation](https://docs.copilotkit.ai)
- [CopilotKit GitHub Repository](https://github.com/CopilotKit/CopilotKit)
- [CopilotRuntime Reference](https://docs.copilotkit.ai/reference/v1/classes/CopilotRuntime)
- [CopilotKit Self Hosting Guide](https://docs.copilotkit.ai/guides/self-hosting)
- [CopilotKit Security Guide](https://docs.copilotkit.ai/guides/security)
- [ClawHub Skill Page](https://clawhub.ai/generaljerel/skills/copilotkit-runtime-patterns)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript, TSX, JSON, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only; no direct tool or API execution.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact document version 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
