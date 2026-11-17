## Description:

Read-only Api3 feed discovery, readiness, coverage, and purchase-planning skill for downstream agent projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daav3](https://clawhub.ai/user/daav3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to discover and verify Api3 decentralized data feeds, inspect activation or runway state, audit chain coverage, and prepare reviewable browser or contract-call plans without giving the skill wallet authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated contract targets, values, or calldata may be stale or unsuitable if used directly for execution.

Mitigation: Review every generated target, value, and calldata field, then run a fresh post-action check before handing details to a wallet or executor.

Risk: RPC or public network data may be unavailable, stale, or supplied by an untrusted endpoint.

Mitigation: Use trusted RPC endpoints and scope installation to read-only network access.

Risk: Supply-chain assurance is weaker because dependencies are declared with version ranges and no committed lockfile is present in the artifact.

Mitigation: Prefer a release with pinned dependencies and a committed lockfile for stronger assurance.

## Reference(s):

- [Project homepage](https://github.com/daav3/agentic-lending-project)
- [ClawHub skill page](https://clawhub.ai/daav3/skills/api3-feed-manager-readonly)
- [Api3 Market](https://market.api3.org)
- [Api3 dAPI pricing data](https://api3dao.github.io/data-feeds/market/dapi-pricing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-like command results and reviewable contract-call details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only outputs; generated calldata and browser plans are review material for a separate human operator, wallet, or executor.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
