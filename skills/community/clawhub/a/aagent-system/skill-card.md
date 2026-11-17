## Description:

A multi-agent automation system for AI Agent skill sample collection, security scanning, threat intelligence collection, and research analysis.

This skill is for research and development only.

## Publisher:

[caidongyun](https://clawhub.ai/user/caidongyun)

### License/Terms of Use:

MIT-0

## Use Case:

Security researchers and developers use this skill to collect AI-agent skill samples, scan them for suspicious or malicious indicators, store local research datasets, and monitor collection performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review classified the skill as suspicious because it can run unreviewed local shell scripts.

Mitigation: Review or replace the referenced local scripts before installation, and execute the skill only in a sandboxed research environment.

Risk: The system can create long-running collection processes that continuously make outbound registry requests and write local datasets.

Mitigation: Apply network, process, runtime, and storage limits before starting the agent manager or orchestrator.

## Reference(s):

- [Aagent System ClawHub Skill Page](https://clawhub.ai/caidongyun/skills/aagent-system)
- [Architecture Notes](artifact/ARCHITECTURE.md)
- [Collection Targets](artifact/TARGET.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command triggers, shell commands, and local JSON data outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local JSON datasets for samples, scan results, malicious findings, performance statistics, evolution history, and orchestrator status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
