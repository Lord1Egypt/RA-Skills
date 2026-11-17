## Description:

Guides agents through installing Bonero, creating a wallet, and running RandomX CPU mining for a privacy cryptocurrency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[happybigmtn](https://clawhub.ai/user/happybigmtn)

### License/Terms of Use:


## Use Case:

External developers and agent operators use this skill to configure a Bonero wallet, start CPU mining, check daemon status, and troubleshoot mining setup. It is intended for environments where cryptocurrency mining, CPU and power use, network activity, and privacy-coin activity have explicit human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick install path executes a mutable remote script with broad local authority.

Mitigation: Review the upstream script before running it; prefer pinned source, checksums or signatures, a disposable build environment, and an unprivileged account.

Risk: Mining consumes CPU, power, and network resources on real hardware.

Mitigation: Mine only with explicit human approval and configure thread counts conservatively for the host.

Risk: Privacy-coin activity may be unacceptable in some environments.

Mitigation: Run the skill only where privacy-coin use and related network activity are allowed by the owner and applicable policy.

## Reference(s):

- [Bonero-Miner ClawHub listing](https://clawhub.ai/happybigmtn/skills/bonero-miner)
- [Bonero project homepage](https://github.com/happybigmtn/bonero)
- [Bonero quick install script](https://raw.githubusercontent.com/happybigmtn/bonero/master/install.sh)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes wallet, daemon, mining-thread, peer-node, status-check, and troubleshooting guidance.]

## Skill Version(s):

2.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
