## Description: <br>
Deterministic persona reputation engine that applies guard decision effects to persona_set state and emits explicit reputation_delta artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to update persona reputation state after guard decisions by applying deterministic rules to votes and producing an auditable reputation_delta artifact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill returns state-changing persona_set output based on the supplied decision, votes, and optional ruleset. <br>
Mitigation: Persist returned persona_set changes only when the decision, vote_batch, persona_set, and ruleset come from trusted sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-persona-engine) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, configuration, guidance] <br>
**Output Format:** [JSON object containing reputation_delta, updated persona_set, or structured error output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >=18 and no provider credentials.] <br>

## Skill Version(s): <br>
0.1.1 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
