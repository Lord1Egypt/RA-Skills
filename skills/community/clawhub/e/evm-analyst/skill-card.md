## Description: <br>
Analyze Polygon EVM fund-flow patterns from seed addresses, transaction hashes, and Dune log outputs using fixed registered Dune queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leon5876](https://clawhub.ai/user/leon5876) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and investigators use this skill to reconstruct Polygon EVM fund flows, annotate event patterns, classify transactions, and identify follow-up Dune queries without fabricating missing blockchain facts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Addresses, transaction hashes, or topic hashes submitted to external blockchain analytics or signature lookup services may disclose sensitive investigative interest. <br>
Mitigation: Avoid submitting sensitive identifiers whose association with the work must remain private, and review the registered Dune queries before use. <br>
Risk: Incomplete Dune query registration can prevent analysis or encourage unsupported assumptions. <br>
Mitigation: Use only registered Dune query codes and return next_query_plan when required data is unavailable. <br>
Risk: Blockchain event interpretation can be misleading when raw logs are incomplete or topic0 signatures are unknown. <br>
Mitigation: Preserve raw evidence fields, mark unknown topic0 values as unknown_event_signature, and avoid fabricating amounts, labels, relationships, or transaction counts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/leon5876/evm-analyst) <br>
- [Dune Query Registry](references/dune_query_registry.md) <br>
- [Topic0 Dictionary](references/topic0_dictionary.md) <br>
- [OpenChain Signature Database Lookup API](https://api.openchain.xyz/signature-database/v1/lookup) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Concise structured Markdown tables such as addresses, patterns, flow_edges, log_annotations, tx_classification, accounting_summary, discovered_addresses, and next_query_plan.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses registered Dune query codes and preserves raw transaction evidence when available; emits next_query_plan when data is insufficient.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact package reports 0.2.1-slim) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
