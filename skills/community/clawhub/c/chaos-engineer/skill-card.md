## Description: <br>
Use when designing chaos experiments, implementing failure injection frameworks, or conducting game day exercises. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lhwa8685](https://clawhub.ai/user/lhwa8685) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, SREs, and DevOps engineers use this skill to design controlled chaos experiments, implement failure injection workflows, conduct game days, define blast radius controls, and document resilience improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Copyable chaos-engineering examples can disrupt production systems or delete live resources. <br>
Mitigation: Run examples only in staging or isolated test environments unless explicit approval, blast-radius limits, monitoring, and rollback controls are in place. <br>
Risk: Failure injection commands may require powerful infrastructure credentials. <br>
Mitigation: Use least-privilege credentials, dry-run steps where supported, and target disposable or narrowly scoped resources. <br>
Risk: Host-wide DNS or network changes can affect unrelated workloads. <br>
Mitigation: Avoid broad host-level changes outside disposable environments and prefer scoped experiment tooling with automated rollback. <br>


## Reference(s): <br>
- [Chaos Engineering Tools & Automation](references/chaos-tools.md) <br>
- [Chaos Experiment Design](references/experiment-design.md) <br>
- [Game Day Planning & Execution](references/game-days.md) <br>
- [Infrastructure Chaos Engineering](references/infrastructure-chaos.md) <br>
- [Kubernetes Chaos Engineering](references/kubernetes-chaos.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks, YAML manifests, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include experiment designs, monitoring and alert configuration, rollback procedures, and learning summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
