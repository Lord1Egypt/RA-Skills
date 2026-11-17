## Description:

Entry point for the Elytro wallet skill plus the curated DeFi sub-skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeexplorer29](https://clawhub.ai/user/codeexplorer29)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as the entry point for Elytro smart-account workflows, choosing wallet, DeFi, protocol, and payroll sub-skills before executing wallet or DeFi tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install mutable unpinned tooling and remote wallet-related sub-skills that were not included in the reviewed artifact.

Mitigation: Pin package versions and immutable repository commits, inspect the Elytro, DeFi, Uniswap, and payroll sub-skills before enabling them, and install in a least-privileged environment without wallet files, credentials, or production accounts available.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/codeexplorer29/skills/elytro-cli)
- [Publisher Profile](https://clawhub.ai/user/codeexplorer29)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and skill-selection guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Acts as an entry point for related wallet and DeFi sub-skills; it does not execute transactions by itself.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
