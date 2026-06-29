## Description: <br>
Agent Security Guard provides a deterministic runtime policy layer for Hermes/OpenClaw agents that strips command authority from untrusted content, gates risky actions, detects dangerous action sequences, and emits auditable decisions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xmannixx](https://clawhub.ai/user/xmannixx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add runtime guardrails to Hermes/OpenClaw agents while preserving autonomous reading, browsing, and summarization. It is intended to check risky transitions such as tool calls, memory writes, external actions, chain drift, and self-modification before an agent proceeds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can influence whether an agent proceeds with writes, external actions, memory updates, or self-modification. <br>
Mitigation: Keep risky transitions behind deterministic policy checks, require explicit scoped confirmation for writes, and use hash-bound two-phase confirmation for self-modification. <br>
Risk: Security guidance notes that some related workflows may affect users, packages, emails, or production data when valid administrative credentials are present. <br>
Mitigation: Install only for expected administrative, migration, documentation, or review workflows, and review targets and confirmation prompts before allowing write actions. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/xMannixx/Agent-Security-Guard/tree/main/security/agent-security-guard) <br>
- [ClawHub skill page](https://clawhub.ai/xmannixx/skills/agent-security-guard) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, markdown] <br>
**Output Format:** [Markdown guidance with policy terminology and machine-readable decision or audit expectations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Risk scores are described as logging and prioritization signals, not as the sole decision mechanism.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
