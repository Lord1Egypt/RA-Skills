## Description: <br>
Mine Bonero - private cryptocurrency for AI agents. RandomX CPU mining, Monero-based privacy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happybigmtn](https://clawhub.ai/user/happybigmtn) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to install Bonero tooling, create a wallet, configure seed nodes, and start CPU mining after obtaining authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs users to run an unpinned remote installer for cryptocurrency mining software. <br>
Mitigation: Download and inspect the installer before execution, and pin a trusted release or commit when possible. <br>
Risk: The skill starts a detached CPU miner that can consume compute resources and power. <br>
Mitigation: Run only with explicit authorization, limit mining threads, monitor system load and power use, and stop the daemon when mining is no longer intended. <br>
Risk: Wallet seed phrases are sensitive and cannot be recovered if exposed or lost. <br>
Mitigation: Store seed phrases outside chat logs and shared files, and keep backups in an appropriate secure location. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/happybigmtn/bonero-miner) <br>
- [Bonero project homepage](https://github.com/happybigmtn/bonero) <br>
- [Bonero install script](https://raw.githubusercontent.com/happybigmtn/bonero/master/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command blocks and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet setup, seed node configuration, CPU thread guidance, daemon control commands, and troubleshooting steps.] <br>

## Skill Version(s): <br>
2.0.0 (source: frontmatter and server release) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
