## Description: <br>
Shared deterministic guard primitives for the Consensus.Tools skill family: hard-block taxonomy, weighted vote aggregation, reputation updates, idempotency keys, strict schema enforcement, and indexed board artifact access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill as shared policy infrastructure for Consensus guard workflows that need deterministic vote aggregation, reputation updates, idempotency keys, strict schema checks, and board artifact access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local board or state writes can influence later consensus decisions when write helpers are called. <br>
Mitigation: Set CONSENSUS_STATE_ROOT to a dedicated non-privileged directory and allow only trusted workflows to call writeArtifact or writeDecision. <br>
Risk: Transitive package behavior may affect a shared policy library used by multiple guards. <br>
Mitigation: Install from a trusted package source, use the lockfile or exact dependency pins, and audit transitive dependencies before production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-guard-core) <br>
- [README](README.md) <br>
- [Security Assurance](SECURITY-ASSURANCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [code, configuration, guidance] <br>
**Output Format:** [JavaScript module exports and structured JSON objects, with Markdown documentation for usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write board or state artifacts under the configured consensus state path when callers use write helpers.] <br>

## Skill Version(s): <br>
1.1.13 (source: package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
