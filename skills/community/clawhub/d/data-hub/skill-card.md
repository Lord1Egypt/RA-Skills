## Description:

Data Hub provides an asynchronous in-memory sharing layer for multi-agent digital-asset trading systems across market state, indicators, intelligence, and risk audit namespaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnny-ggao](https://clawhub.ai/user/johnny-ggao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-agent operators use Data Hub to let orchestrator, analyst, and guard agents write and read shared real-time context with namespace permissions and Pydantic validation. It is not intended for historical storage, market data sourcing, or direct trading execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent_ID namespace checks are not a real security boundary.

Mitigation: Run the skill only inside a trusted agent process and enforce caller identity and authorization before invoking write operations.

Risk: Risk-audit data can be persisted even though the skill is primarily described as in-memory.

Mitigation: Use path-scoped snapshot storage, retention controls, and review stored risk data before production use.

Risk: Mutable read results can let consumers accidentally alter shared state.

Mitigation: Return deep copies or immutable views from read paths before relying on the hub across trust boundaries.

Risk: Large numbers of symbols, payloads, or stored entries can increase memory use.

Mitigation: Apply quotas for symbols, payload size, and stored entries in the calling system.

## Reference(s):

- [ClawHub Data Hub release page](https://clawhub.ai/johnny-ggao/skills/data-hub)
- [Data Hub skill documentation](docs/Data_Hub_Skill.md)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Python package interfaces and structured JSON-like result dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores shared in-memory state by namespace and can optionally write risk-audit snapshots when configured.]

## Skill Version(s):

1.0.0 (source: release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
