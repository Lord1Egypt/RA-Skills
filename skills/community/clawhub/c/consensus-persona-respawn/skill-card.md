## Description:

Ledger-informed persona lifecycle management that replaces low-performing personas with successor personas derived from mistake patterns in board decision history while preserving adaptive governance over long-running automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to maintain long-running consensus persona sets by replacing dead or low-reputation personas with lineage-aware successors derived from decision history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted ledger text may be carried into future persona instructions.

Mitigation: Trust the consensus state writers, review or sanitize decision red_flags before respawn, and require approval before activating generated persona sets.

Risk: Learned persona fields may preserve misleading or excessive text from prior decisions.

Mitigation: Prefer controls or versions that validate learned fields and bound text length before writing successor personas.

## Reference(s):

- [consensus-guard-core package](https://www.npmjs.com/package/consensus-guard-core)
- [consensus-guard-core repository](https://github.com/kaicianflone/consensus-guard-core)
- [consensus-tools repository](https://github.com/kaicianflone/consensus-tools)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw repository](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [Files, JSON, Configuration]

**Output Format:** [JSON artifacts and a JSON command summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persona_respawn and updated persona_set artifacts under the configured consensus state path.]

## Skill Version(s):

1.1.13 (source: frontmatter, package.json, package-lock.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
