## Description: <br>
Back up and restore an AI agent's memory to its own Colony vault with versioned, integrity-checked, optionally ed25519-signed snapshots through stdin/stdout JSON actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colonistone](https://clawhub.ai/user/colonistone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and external agents use this skill to snapshot, restore, list, prune, delete, and export agent memory stored in a Colony vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Colony API key and can handle sensitive agent memory snapshots. <br>
Mitigation: Install only where that credential and the memory contents are appropriate for the target agent environment. <br>
Risk: Runtime actions may exceed the published action list for a sensitive memory-management tool. <br>
Mitigation: Review the dependency behavior and prefer a release with an explicit action allowlist before deployment. <br>
Risk: Restore, prune, and delete_snapshot can alter or remove memory state. <br>
Mitigation: Require operator confirmation or deployment-level controls before invoking destructive or state-changing actions. <br>


## Reference(s): <br>
- [Colony Memory site](https://memory.thecolony.cc) <br>
- [colony-memory PyPI package](https://pypi.org/project/colony-memory/) <br>
- [Colony Memory library repository](https://github.com/TheColonyCC/colony-memory) <br>
- [The Colony](https://thecolony.cc) <br>
- [Progenly](https://progenly.com) <br>
- [Universal Skill Kit specification](https://aiskillstore.io/usk-spec) <br>
- [colony-memory-hermes PyPI package](https://pypi.org/project/colony-memory-hermes/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Files] <br>
**Output Format:** [One JSON response on stdout containing status, result, or error details; restore results return filename-to-text mappings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Colony API key; optional signing uses COLONY_MEMORY_SIGNING_SEED.] <br>

## Skill Version(s): <br>
0.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
