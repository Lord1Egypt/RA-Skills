## Description:

Discover, activate, fund, and maintain Api3 data feeds permissionlessly for downstream agent projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daav3](https://clawhub.ai/user/daav3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Api3 oracle feeds, inspect whether they are active and funded, plan maintenance runway, and execute guarded feed activation or top-up flows when explicitly approved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signer-backed execution can expose private keys when raw key material is passed as a command argument.

Mitigation: Use dry-run planning first and prefer an isolated test wallet or safer signer flow; avoid passing valuable wallet private keys on the command line.

Risk: A submitted blockchain transaction can be reported before final confirmation or before feed readiness is independently verified.

Mitigation: Treat submitted transaction hashes as pending until receipt status and on-chain feed readiness are confirmed.

Risk: Not every Api3 funding path is fully executable by the bundled runtime.

Mitigation: Review the funding classification and use browser-assisted or unsupported-path guidance where exact execution is not available.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daav3/skills/api3-feed-manager)
- [Project homepage](https://github.com/daav3/agentic-lending-project)
- [Api3 dApp quickstart](https://docs.api3.org/dapps/quickstart/)
- [Api3 dApp integration](https://docs.api3.org/dapps/integration/)
- [Api3 contract integration](https://docs.api3.org/dapps/integration/contract-integration.html)
- [Api3 OEV rewards](https://docs.api3.org/dapps/oev-rewards/)
- [Api3 data feeds for OEV searchers](https://docs.api3.org/oev-searchers/in-depth/data-feeds/)
- [Api3 Market](https://market.api3.org)
- [Api3 dAPI pricing data feeds](https://api3dao.github.io/data-feeds/market/dapi-pricing)
- [Part 1 Architecture Update](references/part1-architecture-update.md)
- [Part 1 Research](references/part1-research.md)
- [Part 1 Skill Spec](references/part1-skill-spec.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured status fields and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include feed identifiers, chain status, funding estimates, transaction plans, submitted transaction hashes, maintenance recommendations, and warnings.]

## Skill Version(s):

0.4.4 (source: release evidence, package.json, changelog released 2026-05-19)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
