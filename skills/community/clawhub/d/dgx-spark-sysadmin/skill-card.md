## Description:

Administer DGX Spark hosts safely through remote access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cbertucci33](https://clawhub.ai/user/cbertucci33)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and infrastructure operators use this skill to manage authorized DGX Spark hosts over SSH, including access setup, ConnectX-7 fabric validation, monitoring, rolling restarts, reboots, and coordinated system updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact administration actions can interrupt DGX Spark hosts, networking, or workloads.

Mitigation: Require explicit approval, scope, interruption expectations, success gates, rollback, and an independent recovery path before disruptive procedures.

Risk: Secrets such as private keys, Tailscale auth keys, tokens, or passwords could be exposed during remote setup.

Mitigation: Keep secrets out of prompts, command arguments, logs, and files; transfer only public keys through trusted paths.

Risk: Multi-node changes can leave hosts inconsistent or unreachable.

Mitigation: Apply one state change at a time, avoid simultaneous reboots, verify every affected node, and reconcile partial success before continuing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cbertucci33/skills/dgx-spark-sysadmin)
- [Server-resolved source repository](https://github.com/cbertucci33/dgx-spark-sysadmin)
- [NVIDIA DGX Spark User Guide](https://docs.nvidia.com/dgx/dgx-spark/)
- [DGX Spark OS and Component Update Guide](https://docs.nvidia.com/dgx/dgx-spark/os-and-component-update.html)
- [DGX Spark Clustering Guide](https://docs.nvidia.com/dgx/dgx-spark/spark-clustering.html)
- [NVIDIA Connect Two Sparks playbook](https://build.nvidia.com/spark/connect-two-sparks)
- [NVIDIA NCCL for DGX Spark playbook](https://build.nvidia.com/spark/nccl)
- [Tailscale Linux installation](https://tailscale.com/docs/install/linux)
- [Tailscale MagicDNS](https://tailscale.com/docs/features/magicdns)
- [Tailscale SSH](https://tailscale.com/docs/features/tailscale-ssh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, checklists, and verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an ssh client and authorized access to target DGX Spark systems.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
