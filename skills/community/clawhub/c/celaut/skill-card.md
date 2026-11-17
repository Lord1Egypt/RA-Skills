## Description:

Celaut Skill gives agents guidance to install and administer Nodo, package content-addressed Celaut services, run and observe microVM workloads, and discover on-chain Unstoppable Skills through a read-only MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xf965](https://clawhub.ai/user/0xf965)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to work with the Celaut decentralized-compute ecosystem: installing Nodo, preparing service packages, executing workloads, observing runtime behavior, and reading the Skills registry.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents installing and running mutable network-sourced code with high host privileges.

Mitigation: Use a dedicated Linux host or VM, pin source commits, verify checksums or signatures where available, and require human review before any sudo command or installer execution.

Risk: Wallet mnemonics and Ergo transactions can expose self-custodied funds, and transactions are final and irreversible.

Mitigation: Never configure wallet mnemonics, initiate Ergo spending, or submit reputation/payment transactions without explicit review and consent; keep wallet secrets out of repositories and agent logs.

Risk: Running Celaut workloads can consume gas or resources and may execute third-party service packages.

Mitigation: Inspect service declarations, run feasibility and cost estimation before execution, pass only declared environment variables, and monitor or stop instances deliberately.

## Reference(s):

- [Celaut Skill on ClawHub](https://clawhub.ai/0xf965/skills/celaut)
- [Celaut Paradigm](https://github.com/celaut-project/paradigm)
- [Celaut Nodo Repository](https://github.com/celaut-project/nodo)
- [Celaut Skills Repository](https://github.com/celaut-project/skills)
- [Celaut Skills README](https://github.com/celaut-project/skills/blob/main/README.md)
- [Celaut Skills MCP Specification](https://github.com/celaut-project/skills/blob/main/MCP.md)
- [Nodo Stable README](https://github.com/celaut-project/nodo/blob/stable/README.md)
- [Nodo Configuration Example](https://github.com/celaut-project/nodo/blob/stable/config.example.yaml)
- [Ergo Manifesto](https://ergoplatform.org/en/blog/2021-04-26-the-ergo-manifesto/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance for terminal-first Celaut and Nodo workflows; no autonomous blockchain spending should occur without explicit user consent.]

## Skill Version(s):

1.2.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
