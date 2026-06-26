## Description: <br>
Consul CLI command reference for service discovery, key-value store, health checks, cluster management, and service mesh operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonasgao](https://clawhub.ai/user/jonasgao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill as a Consul CLI reference when managing agents, service discovery, key-value operations, ACLs, cluster operations, snapshots, and service mesh workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutating Consul administration commands can alter cluster state, remove services or keys, restore snapshots, or change Raft membership. <br>
Mitigation: Confirm the cluster, datacenter, namespace, token, target nodes, and backup state before execution; require explicit approval for recursive deletes, snapshot restores, force-leave, Raft changes, service deregistration, locks, watch handlers, consul exec, and writes under `/etc`. <br>
Risk: ACL root tokens, SecretIDs, cloud join secrets, and TLS material may be exposed if pasted into chat logs or shell history. <br>
Mitigation: Keep secrets out of prompts, logs, and command history; prefer token files or secure secret stores and redact sensitive command examples before sharing. <br>


## Reference(s): <br>
- [Consul CLI Reference](references/cli-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with CLI examples, command snippets, configuration samples, and reference tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not install or run hidden code; outputs should be reviewed before executing mutating Consul administration commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
