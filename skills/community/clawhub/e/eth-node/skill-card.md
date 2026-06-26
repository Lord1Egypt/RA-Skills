## Description: <br>
Manage Ethereum execution client nodes, including start and stop workflows, sync status, peers, logs, and configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[apexfork](https://clawhub.ai/user/apexfork) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and node operators use this skill to administer local Ethereum execution clients such as reth and geth, check sync and peer health, inspect logs, and apply basic node configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exposing Ethereum RPC or admin/debug/trace namespaces to a public network can allow unauthorized node inspection or manipulation. <br>
Mitigation: Keep RPC bound to 127.0.0.1, avoid public admin/debug/trace exposure, and use a firewall before any non-local access. <br>
Risk: Running execution clients in the background can consume significant disk, CPU, memory, and network resources. <br>
Mitigation: Monitor node resource use and logs while syncing or troubleshooting. <br>
Risk: Installing clients directly from package managers or source can introduce version drift or unreviewed updates. <br>
Mitigation: Use official releases where possible and consider pinning client versions for production node operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/apexfork/eth-node) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>
- [reth project](https://github.com/paradigmxyz/reth) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-RPC examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local node process state, logs, and RPC responses when the agent is used in an environment with an Ethereum execution client.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
