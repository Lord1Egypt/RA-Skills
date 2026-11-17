## Description:

Provides a six-item self-check before smart-contract interactions, covering audits, contract addresses, allowances, revocation, private-key custody, and small test transactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0 (release metadata); MIT for Python code; documentation and theory all rights reserved

## Use Case:

Developers and other smart-contract users can review six safety checks before approving funds or interacting with a contract. Results reflect the items they report as completed, not an independent audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared Write and WebFetch access exceeds the checklist's apparent needs and conflicts with its no-network/no-filesystem claims.

Mitigation: Review before installation and remove Write and WebFetch permissions unless they are justified.

Risk: The usage instructions mention command-line options the script does not accept.

Mitigation: Use the script's supported --have, --approve, and --json options; align the published instructions with them.

Risk: A PASS result relies on self-reported completion of checks rather than independent verification.

Mitigation: Verify contract addresses, audits, and authorization details independently before moving funds.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/contract-interact-checklist)
- [Skill README](README.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain-text checklist or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports PASS or FAIL, missing checks, and an exit status.]

## Skill Version(s):

1.0.5 (source: ClawHub release; bundled SKILL.md lists 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
