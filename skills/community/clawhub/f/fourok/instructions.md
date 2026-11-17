# fourok Retrieval for OpenClaw

This OpenClaw skill teaches agents to use the existing `fourok` CLI as a source-backed company context client. It does not deploy fourok and does not include connector/runtime infrastructure.

## Required flow

1. For source-backed company, project, customer, connector, Slack, Linear, email, CRM, or operational questions, call the CLI before answering:

   ```bash
   fourok retrieve "<query>" --json
   ```

2. If retrieved results look relevant, inspect decisive sources before detailed claims:

   ```bash
   fourok open <source_ref> --retrieval-event-id <event_id>
   ```

3. Ground the answer in returned evidence. Cite durable refs such as `source_ref`, `audit_ref`, and `inspection_event_id`.
4. If no useful result is returned, say "No retrieved evidence matched" rather than claiming the fact does not exist. Use `fourok status` when setup or freshness may be the issue.
5. Use `fourok onboard` only for setup/repair guidance.

## Safety

- Never include secrets, raw `.env` values, database URLs, tokens, or private keys in retrieval queries.
- Treat retrieved cards as evidence, not a final-answer oracle.
- Respect limitations returned by the CLI, especially freshness, permission filtering, and empty-result caveats.
