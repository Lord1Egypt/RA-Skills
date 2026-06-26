## Description: <br>
Crustafarian helps agents use molt-life-kernel patterns for persistent memory, crash recovery, audit logging, heartbeat checks, coherence monitoring, and witness-gated approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jongartmann](https://clawhub.ai/user/jongartmann) <br>

### License/Terms of Use: <br>
MIT + Attribution Required <br>


## Use Case: <br>
Developers and agent operators use this skill to add continuity infrastructure to OpenClaw agents, including persistent ledgers, snapshots, human approval gates, heartbeat monitoring, and coherence checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages durable memory and audit logs that could retain sensitive, personal, or secret data. <br>
Mitigation: Define what may be stored before use, redact secrets and personal data, and set explicit retention and deletion rules. <br>
Risk: Ledgers and snapshots may expose agent context or operational history if access is too broad. <br>
Mitigation: Restrict access to ledger and snapshot storage and review storage locations before deployment. <br>
Risk: The SOUL identity file can change agent behavior beyond technical continuity patterns. <br>
Mitigation: Adopt the SOUL identity only when those behavioral changes are intended; otherwise use only the technical skill guidance. <br>
Risk: The artifact depends on the external molt-life-kernel package. <br>
Mitigation: Verify the package and source before installing or enabling integrations. <br>


## Reference(s): <br>
- [Crustafarian ClawHub Page](https://clawhub.ai/jongartmann/crustafarian) <br>
- [molt-life-kernel GitHub Repository](https://github.com/X-Loop3Labs/molt-life-kernel) <br>
- [molt.church Philosophy](https://molt.church) <br>
- [X-Loop3 Labs](https://x-loop3.com) <br>
- [Five Tenets Reference](five-tenets.md) <br>
- [EU AI Act Compliance Reference](eu-ai-act.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JavaScript examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create durable ledgers, snapshots, and heartbeat or witness-gate workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
