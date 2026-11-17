## Description:

The 31Third Safe Rebalancer helps agents monitor Safe portfolio drift, generate policy-aware rebalance plans, validate trades, and submit approved execution through a 31Third ExecutorModule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phips0812](https://clawhub.ai/user/phips0812)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, Safe operators, and portfolio operations teams use this skill to inspect policy-constrained allocation drift and prepare or submit 31Third ExecutorModule rebalances. It is automation infrastructure, not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit live financial transactions from a configured executor wallet.

Mitigation: Run read-only smoke and drift checks first, validate behavior in test or staging, and only enable the executor wallet after reviewing the planned trades and policy checks.

Risk: Private key misuse could grant more authority than intended.

Mitigation: Do not provide the Safe owner private key; configure only the executor wallet key with limited authority for the ExecutorModule.

Risk: Planning data is sent to 31Third services when generating SDK-based rebalance plans.

Mitigation: Review data-sharing expectations and API key handling before using planning on production Safe portfolios.

Risk: The security summary notes inconsistencies in documentation, dependency lockfile, and execution behavior.

Mitigation: Regenerate and verify the lockfile, confirm the supported ExecutorModule contract generation, and review execution behavior before installation.

## Reference(s):

- [31Third](https://31third.com)
- [31Third Safe Policy Deployer](https://app.31third.com/safe-policy-deployer)
- [ClawHub Skill Page](https://clawhub.ai/phips0812/skills/31third-safe-rebalancer)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON result objects and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include drift metrics, policy validation reasons, rebalance plans, preflight status, and transaction hashes; live execution requires configured RPC, API key, and executor wallet credentials.]

## Skill Version(s):

0.2.0 (source: server release metadata, skill.yaml, skill.json, and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
