## Description:

AI-native company intelligence engine with 8-step metabolic pipeline, cross-file inference, neural chain design, and information classification routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ygq19901001](https://clawhub.ai/user/ygq19901001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and business operations teams use this skill to turn company signals, departmental reports, and external inputs into classified intelligence, cross-file inferences, prioritized actions, and routing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to handle company-sensitive information and route it across local, shared, cloud, and model-processing paths.

Mitigation: Require classification-aware routing before any cloud copy, shared-folder write, model call, or log entry.

Risk: Broad logging and automatic mirroring can expose sensitive message content if deployed without review.

Mitigation: Avoid logging full message bodies by default and review mirroring rules before installing in a real business environment.

Risk: Scheduled deletion could remove records needed for legal, audit, incident, or recovery purposes.

Mitigation: Make raw-data deletion opt-in and define retention exceptions before enabling cleanup automation.

## Reference(s):

- [8-Step Metabolic Pipeline Operations Playbook](artifact/references/pipeline-playbook.md)
- [Cross-File Inference Patterns](artifact/references/inference-patterns.md)
- [Neural Chain Design](artifact/references/neural-chain-design.md)
- [Server-Resolved GitHub Provenance](https://github.com/Ygq19901001/biobrain-intelligence-brain)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with structured examples and operational checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes classification-aware routing, SLA guidance, cross-file inference patterns, and operational review checkpoints.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
