## Description:

Analyze Polygon EVM fund-flow patterns from seed addresses, tx hashes, and Dune log outputs. Use fixed registered Dune queries only.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leon5876](https://clawhub.ai/user/leon5876)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, investigators, and analysts use this skill to reconstruct Polygon EVM fund flows from seed addresses, transaction hashes, decoded logs, raw polygon.logs rows, and Dune query results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis may send public blockchain identifiers, transaction hashes, query parameters, and unknown topic0 hashes to Dune or OpenChain.

Mitigation: Use the skill only when those external services may see the lookup pattern, and avoid sensitive private investigation context unless that exposure is acceptable.

Risk: Unsupported or missing Dune queries could lead to invented query IDs, dynamic SQL, or incomplete data collection.

Mitigation: Use only registered query IDs from the Dune Query Registry and emit next_query_plan when the needed query type is missing.

Risk: Insufficient logs, unknown event signatures, or ambiguous protocol behavior can produce misleading fund-flow or accounting classifications.

Mitigation: Preserve raw evidence in structured rows, mark unknown topic0 values explicitly, and output next_query_plan instead of guessing when data is insufficient.

## Reference(s):

- [Dune Query Registry](artifact/references/dune_query_registry.md)
- [Topic0 Dictionary](artifact/references/topic0_dictionary.md)
- [OpenChain Signature Database API](https://api.openchain.xyz/signature-database/v1/lookup)
- [ClawHub Skill Page](https://clawhub.ai/leon5876/skills/evm-analyst)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise Markdown tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Structured tables for addresses, patterns, pattern steps, flow edges, log annotations, transaction classification, accounting summaries, discovered addresses, and next query plans.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 0.2.1-slim)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
