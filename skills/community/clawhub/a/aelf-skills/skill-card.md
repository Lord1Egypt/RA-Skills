## Description:

Discovery, download, configuration, and routing hub for aelf ecosystem agent skills across wallets, DEX, NFT marketplace, explorer, governance, and node interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzz780](https://clawhub.ai/user/hzz780)

### License/Terms of Use:

MIT

## Use Case:

External developers and agent operators use this skill to discover aelf ecosystem skills, route aelf-related intents to the right skill, bootstrap selected skills into supported clients, and run health or audit workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bootstrap can act on catalog-controlled skill identifiers and destination paths.

Mitigation: Install only from trusted catalogs, prefer a disposable destination directory, and review selected skill IDs before running bootstrap.

Risk: Bootstrap runs dependency installation on downloaded third-party skill packages by default.

Mitigation: Use --skip-install for review-first workflows and inspect downloaded skill files before running setup or dependency installation.

Risk: Routed skills can lead to blockchain write operations such as transfers, approvals, swaps, trades, or contract sends.

Mitigation: Perform read checks first, prefer simulation or dry-run paths when available, and require explicit user confirmation before write operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hzz780/skills/aelf-skills)
- [Catalog Schema Semantics](docs/CATALOG_SCHEMA.md)
- [Skill Routing Matrix](docs/SKILL_ROUTING_MATRIX.md)
- [AI End-to-End Execution Scenarios](docs/AI_E2E_SCENARIOS.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and routing recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected skill IDs, setup commands, health-check outcomes, and recovery hints.]

## Skill Version(s):

0.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
