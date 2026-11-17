## Description:

Deterministic persona reputation engine that applies guard decision effects to persona_set state and emits explicit reputation_delta artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and governance-tool builders use this skill to apply deterministic reputation updates after a guard decision and vote batch. It returns an explicit reputation_delta artifact and updated persona_set for downstream review or storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reputation rules may encode governance assumptions that are not appropriate for every board or deployment.

Mitigation: Review and tune the ruleset before relying on the output for real governance decisions.

Risk: Invalid or incomplete decision, vote_batch, or persona_set input can produce structured errors or skipped persona updates.

Mitigation: Validate input JSON before invocation and review the emitted reputation_delta before downstream use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/consensus-persona-engine)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON object containing reputation_delta, updated persona_set, or structured error JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Deterministic local Node.js execution; requires node and does not require provider credentials.]

## Skill Version(s):

0.1.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
