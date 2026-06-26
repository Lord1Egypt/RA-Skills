## Description: <br>
Helps agents discover documented BlockPI RPC methods, choose JSON-RPC, HTTP, gRPC, or GraphQL routes, estimate RU usage, persist endpoints locally, and make user-directed calls with user-provided BlockPI endpoints or tokens. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neganzhao](https://clawhub.ai/user/neganzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and blockchain operators use this skill to validate documented BlockPI methods, choose the right transport for a chain, estimate request-unit impact, and prepare or execute live RPC calls through user-provided BlockPI credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: BlockPI endpoints and tokens may be sensitive local runtime data. <br>
Mitigation: Keep the state/ directory private, avoid sharing real endpoints or keys in chats, and do not commit local endpoint state. <br>
Risk: Live blockchain RPC calls may consume request units or submit already-signed transaction data. <br>
Mitigation: Require explicit user-provided endpoints or tokens before live calls, review the method and payload first, and treat RU estimates as guidance rather than final billing truth. <br>
Risk: gRPC execution can expose tokens in local command arguments or grpcurl output. <br>
Mitigation: Treat grpcurl tokens, proto paths, and output as sensitive runtime material and review commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neganzhao/blockpi-rpc-skill) <br>
- [BlockPI Dashboard](https://dashboard.blockpi.io/) <br>
- [BlockPI pricing](https://blockpi.io/pricing/) <br>
- [BlockPI Protocol Catalog Summary](references/rpc_summary.md) <br>
- [BlockPI Protocol Matrix](references/protocol_matrix.md) <br>
- [BlockPI RPC Catalog](references/rpc_catalog.json) <br>
- [Request Unit Pricing Notes](references/pricing_notes.md) <br>
- [Solana Yellowstone gRPC Design Notes](references/solana-yellowstone-design.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown guidance with command examples, JSON request payloads, and user-directed RPC/API responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create encrypted local endpoint state under state/ when the user approves endpoint persistence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
