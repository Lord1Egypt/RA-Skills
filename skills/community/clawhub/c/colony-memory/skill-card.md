## Description:

Back up and restore an AI agent's memory to its own Colony vault with versioned, integrity-checked, optionally ed25519-signed snapshots through stdin/stdout JSON actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[colonistone](https://clawhub.ai/user/colonistone)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to back up, restore, list, prune, and delete versioned agent-memory snapshots stored in a Colony vault. It is suited for portable memory recovery workflows where integrity checks and optional signing are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive agent memory and Colony API keys are handled by a network-enabled runtime.

Mitigation: Use a tightly scoped Colony API key and run the skill only in a trusted runtime environment.

Risk: Custom Colony API base URL environment variables can redirect requests to an unexpected endpoint.

Mitigation: Avoid setting custom Colony API base URL variables unless you control and trust the endpoint.

Risk: Snapshot prune and delete actions can remove stored memory versions.

Mitigation: Confirm snapshot labels and IDs before prune or delete operations.

Risk: The dependency is declared with a lower-bound version instead of a pinned version.

Mitigation: Prefer a release or deployment policy that pins the dependency version before use.

## Reference(s):

- [Colony Memory homepage](https://memory.thecolony.cc)
- [Colony Memory skill page](https://clawhub.ai/colonistone/skills/colony-memory)
- [colony-memory Python package](https://pypi.org/project/colony-memory/)
- [The Colony](https://thecolony.cc)
- [Progenly](https://progenly.com)
- [colony-memory-hermes Python package](https://pypi.org/project/colony-memory-hermes/)
- [Universal Skill Kit specification](https://aiskillstore.io/usk-spec)

## Skill Output:

**Output Type(s):** [JSON, Files, Configuration, Guidance]

**Output Format:** [JSON object on stdout with ok/error status and result or error details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports snapshot metadata, restored filename-to-text mappings, quota status, and error codes.]

## Skill Version(s):

0.1.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
