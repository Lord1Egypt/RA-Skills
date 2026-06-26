## Description: <br>
Generate and persist reusable persona panels (persona_set artifacts) for consensus decision workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to initialize reusable evaluator personas for consensus-based decision workflows. It creates or reuses persona sets with baseline reputation and risk-posture fields, then writes the resulting persona_set artifact to configured board state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes persistent persona_set artifacts to the configured consensus state path. <br>
Mitigation: Set CONSENSUS_STATE_FILE and CONSENSUS_STATE_ROOT to a dedicated non-privileged directory that does not contain secrets, system files, or unrelated project state. <br>
Risk: Reusable persona sets can be reused across later consensus workflows when the existing set matches the requested size, pack, and domain. <br>
Mitigation: Use force_regenerate when a workflow needs a fresh evaluator cohort rather than reusing the latest compatible persona set. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-persona-generator) <br>
- [consensus-guard-core package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Configuration] <br>
**Output Format:** [JSON persona_set artifact with persona metadata and board write reference] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and tsx, plus CONSENSUS_STATE_FILE and CONSENSUS_STATE_ROOT configured to a writable consensus state path.] <br>

## Skill Version(s): <br>
1.1.14 (source: release evidence, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
