## Description: <br>
Bridge skill to install Celaut Nodo, package services, execute decentralized microVM workloads, and discover Unstoppable Skills on-chain or via MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xf965](https://clawhub.ai/user/0xf965) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and manage Celaut Nodo, package Celaut services, run decentralized microVM workloads, and query Celaut Skills through CLI or MCP workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes root-level installation, update, diagnostics, and service-control commands. <br>
Mitigation: Use a dedicated Debian or Ubuntu host, review installer scripts before execution, prefer pinned releases or verified checksums, and require explicit approval before sudo, update, daemon restart, or diagnostic actions. <br>
Risk: The skill can execute decentralized workloads, advertise remote networking, change gas allocation, terminate instances, remove services, and repair registries. <br>
Mitigation: Inspect each service first, run feasibility and cost estimates before execution, and require explicit approval before workload execution, --remote networking, gas changes, kill, remove, or registry repair actions. <br>


## Reference(s): <br>
- [Celaut Skill on ClawHub](https://clawhub.ai/0xf965/skills/celaut) <br>
- [Celaut Nodo Repository](https://github.com/celaut-project/nodo) <br>
- [Nodo User Guide](https://github.com/celaut-project/nodo/blob/master/docs/USAGE.md) <br>
- [Manual Installation Guide](https://github.com/celaut-project/nodo/blob/master/docs/INSTALL.md) <br>
- [Know Your Assumptions](https://github.com/celaut-project/nodo/blob/master/docs/KyA.md) <br>
- [Ergo Blockchain Integration](https://github.com/celaut-project/nodo/blob/master/docs/ERGO.md) <br>
- [Unstoppable Skills README](https://raw.githubusercontent.com/celaut-project/skills/refs/heads/main/README.md) <br>
- [Unstoppable Skills MCP Server Specification](https://raw.githubusercontent.com/celaut-project/skills/refs/heads/main/MCP.md) <br>
- [Agent Skills Format Specification](https://agentskills.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes commands that can install software, manage services, execute workloads, configure networking, and query MCP tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
