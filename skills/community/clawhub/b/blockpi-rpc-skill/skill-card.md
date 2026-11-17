## Description:

Multi-protocol BlockPI access skill for discovering documented methods, routing requests by protocol, mapping RU pricing, and calling BlockPI endpoints across JSON-RPC, HTTP, gRPC, and GraphQL where the official docs support them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neganzhao](https://clawhub.ai/user/neganzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to validate BlockPI-supported methods, choose protocol-aware access paths, estimate documentation-based RU costs, and prepare or execute calls against user-provided BlockPI endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret-bearing BlockPI endpoints or tokens may be exposed during chat, debug, or metadata output.

Mitigation: Use short-lived, least-privileged keys, avoid pasting full secret-bearing endpoints into chat, and avoid debug or metadata output when real credentials are present.

Risk: Live blockchain calls can have high-impact or irreversible effects if signed transactions are broadcast.

Mitigation: Review each action before execution and only allow signed transaction broadcasts when the user explicitly intends that on-chain action.

Risk: Saved endpoint state contains sensitive runtime data.

Mitigation: Keep endpoint state local, do not commit or distribute state files or key material, and re-provide endpoints if local key material is lost.

## Reference(s):

- [BlockPI Protocol Catalog Summary](references/rpc_summary.md)
- [BlockPI Protocol Matrix](references/protocol_matrix.md)
- [BlockPI RPC Catalog](references/rpc_catalog.json)
- [Request Unit Pricing Notes](references/pricing_notes.md)
- [Solana Yellowstone gRPC Design Notes](references/solana-yellowstone-design.md)
- [BlockPI Pricing](https://blockpi.io/pricing/)
- [BlockPI Dashboard](https://dashboard.blockpi.io/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON and shell command snippets; live call results may be JSON or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist local endpoint configuration and may initiate user-requested network calls through the bundled script.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
