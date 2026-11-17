## Description:

Generate and persist reusable persona panels (persona_set artifacts) for consensus decision workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to bootstrap reusable evaluator personas for consensus-based decision workflows, including governance checks for publishing, support, merge, and action decisions. It creates initial persona roles, biases, risk postures, voting styles, and reputation baselines for downstream consensus guards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes consensus state artifacts to the configured state path.

Mitigation: Set CONSENSUS_STATE_FILE or CONSENSUS_STATE_ROOT to a dedicated non-sensitive, non-privileged directory.

Risk: Runtime behavior depends on npm packages installed with the release.

Mitigation: Pin or review dependencies before production use and upgrade them through the normal dependency review process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/consensus-persona-generator)
- [consensus-guard-core package](https://www.npmjs.com/package/consensus-guard-core)
- [consensus-guard-core repository](https://github.com/kaicianflone/consensus-guard-core)
- [Consensus Tools repository](https://github.com/kaicianflone/consensus-tools)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [JSON, Files, Configuration]

**Output Format:** [JSON persona_set artifact with persona_set_id, personas[], and a board_write reference]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and tsx. Reads CONSENSUS_STATE_FILE or CONSENSUS_STATE_ROOT and writes consensus board state artifacts under the configured state path.]

## Skill Version(s):

1.1.14 (source: frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
