---
name: fund-flow-analyst
description: Analyze Polygon EVM fund-flow patterns from seed addresses, tx hashes, and Dune log outputs. Use fixed registered Dune queries only.
version: 0.2.1-slim
---

# Fund Flow Analyst

Use this skill when the user provides Polygon seed addresses, transaction hashes, decoded logs, raw `polygon.logs` rows, or Dune query results and asks for fund-flow reconstruction, pattern annotation, or accounting classification.

## Hard rules

1. Use only registered Dune queries in `references/dune_query_registry.md`. Do not invent query IDs or URLs.
2. Do not fabricate amounts, addresses, relationships, labels, or transaction counts.
3. Do not hard-exclude a transaction merely because it contains a known pattern. Exclude only when all material logs are explained.
4. Same address appears once in `addresses`; pattern differences belong in `flow_edges` and `log_annotations`.
5. `flow_edges` contains only transfer-class events, including mint/burn. Swap, Sync, Approval, and custom events stay in `log_annotations` unless they directly transfer value.
6. One transaction may match multiple patterns.
7. Separate `external_capital_inflow` from `protocol_token_recycle`.
8. If data is insufficient, output `next_query_plan` instead of guessing.
9. For topic0 decoding, use `references/topic0_dictionary.md` when available. Unknown topic0 should be marked `unknown_event_signature`.
10. Preserve raw evidence: include sample tx hash, log index, contract address, topic0, token address, and decoded from/to/amount where available.

## Required output

Keep results concise and structured. Prefer these tables when relevant:

- `addresses`: address, role_guess, evidence, confidence
- `patterns`: pattern_id, pattern_name, description, confidence
- `pattern_steps`: pattern_id, step_no, event_type, contract_address, topic0, meaning
- `flow_edges`: tx_hash, log_index, from_address, to_address, token_contract, amount_raw, amount_normalized, edge_type
- `log_annotations`: tx_hash, log_index, contract_address, topic0, decoded_signature, interpretation
- `tx_classification`: tx_hash, classification, reason, unresolved_items
- `accounting_summary`: bucket, token_contract, gross_in, gross_out, net, notes
- `discovered_addresses`: address, first_seen_tx, reason_to_follow
- `next_query_plan`: query_code, purpose, parameters_needed

Do not output prose-only analysis.
