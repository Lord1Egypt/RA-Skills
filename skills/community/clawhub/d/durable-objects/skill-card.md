## Description:

Create and review Cloudflare Durable Objects for stateful coordination, RPC methods, SQLite storage, alarms, WebSockets, Workers integration, wrangler configuration, and Vitest testing, with a bias toward current Cloudflare documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[creativerezz](https://clawhub.ai/user/creativerezz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, implement, test, and review Cloudflare Durable Objects for stateful Workers applications such as chat rooms, multiplayer games, booking systems, per-tenant storage, alarms, and WebSocket coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Worker or Durable Object examples could expose public APIs without sufficient access control.

Mitigation: Require authentication and object-level authorization for every Durable Object route, using identity from verified sessions or tokens.

Risk: Generated HTTP handlers could allow overly broad cross-origin access or unexpected methods.

Mitigation: Restrict CORS to trusted origins and explicitly reject unsupported HTTP methods before dispatching to Durable Objects.

Risk: Testing setup guidance could leave development dependencies floating.

Mitigation: Pin development dependencies when following the Vitest and Workers testing setup.

Risk: Agent-generated Worker code may be incorrect or unsafe for deployment if copied directly.

Mitigation: Review generated Worker code carefully before deployment.

## Reference(s):

- [Cloudflare Durable Objects documentation](https://developers.cloudflare.com/durable-objects/)
- [Cloudflare Durable Objects API reference](https://developers.cloudflare.com/durable-objects/api/)
- [Cloudflare Durable Objects best practices](https://developers.cloudflare.com/durable-objects/best-practices/)
- [Cloudflare Durable Objects examples](https://developers.cloudflare.com/durable-objects/examples/)
- [Durable Objects rules and best practices](references/rules.md)
- [Testing Durable Objects](references/testing.md)
- [Cloudflare Workers best practices](references/workers.md)
- [durable-utils SQLite schema migrations](https://github.com/lambrospetrou/durable-utils#sqlite-schema-migrations)
- [Cloudflare Actors SQL schema migrations](https://github.com/cloudflare/actors/blob/main/packages/storage/src/sql-schema-migrations.ts)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, JSON, TOML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Durable Object design recommendations, wrangler configuration, testing setup, and code review findings.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
