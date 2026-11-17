## Description:

One-step Safe rebalancer using on-chain 31Third policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phips0812](https://clawhub.ai/user/phips0812)

### License/Terms of Use:

MIT-0

## Use Case:

External Safe operators and developers use this skill to verify a 31Third policy deployment and execute a one-step on-chain rebalance from Safe balances into configured target allocations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute real on-chain rebalancing with an executor private key.

Mitigation: Use a least-privilege executor wallet, keep the Safe owner key out of the tool, run verify-deployment before rebalance_now, and test with minimal value first.

Risk: Secrets such as the executor private key and 31Third API key are required at runtime.

Mitigation: Store secrets outside committed files and provide them through a controlled runtime environment.

Risk: Install metadata is not reproducible enough for a production financial automation workflow.

Mitigation: Regenerate and review the lockfile from the current package.json, prefer npm ci, and pin maintainer CLI tooling before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phips0812/skills/31third-safe-rebalancer-simple)
- [31Third](https://31third.com)
- [31Third Safe Policy Deployer](https://app.31third.com/safe-policy-deployer)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON results and Markdown-readable CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return transaction hashes, deployment verification checks, warnings, and rebalance status messages.]

## Skill Version(s):

0.2.0 (source: server release metadata, package.json, skill.yaml, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
