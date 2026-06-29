## Description: <br>
Create and review Cloudflare Durable Objects for stateful coordination, RPC methods, SQLite storage, alarms, WebSockets, Workers integration, wrangler configuration, and Vitest testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[creativerezz](https://clawhub.ai/user/creativerezz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, implement, test, and review Cloudflare Durable Objects for stateful edge applications such as chat rooms, multiplayer games, booking systems, per-entity storage, and persistent WebSocket coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Production logging examples may expose secrets, auth headers, tokens, raw request bodies, or unnecessary user identifiers if copied without review. <br>
Mitigation: Review logging code before use and redact sensitive request, credential, token, and user-identifying data. <br>
Risk: Wrangler deploy and secret commands operate on real Cloudflare account resources. <br>
Mitigation: Review wrangler configuration, target environment, migrations, and secret commands before applying them. <br>


## Reference(s): <br>
- [ClawHub Durable Objects skill page](https://clawhub.ai/creativerezz/durable-objects) <br>
- [Cloudflare Durable Objects documentation](https://developers.cloudflare.com/durable-objects/) <br>
- [Cloudflare Durable Objects API reference](https://developers.cloudflare.com/durable-objects/api/) <br>
- [Cloudflare Durable Objects best practices](https://developers.cloudflare.com/durable-objects/best-practices/) <br>
- [Cloudflare Durable Objects examples](https://developers.cloudflare.com/durable-objects/examples/) <br>
- [Durable Objects rules and best practices](references/rules.md) <br>
- [Testing Durable Objects](references/testing.md) <br>
- [Cloudflare Workers best practices](references/workers.md) <br>
- [durable-utils SQLite schema migrations](https://github.com/lambrospetrou/durable-utils#sqlite-schema-migrations) <br>
- [Cloudflare Actors SQL schema migrations reference](https://github.com/cloudflare/actors/blob/main/packages/storage/src/sql-schema-migrations.ts) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with TypeScript, JSONC, TOML, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance emphasizes retrieving current Cloudflare documentation before implementation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
