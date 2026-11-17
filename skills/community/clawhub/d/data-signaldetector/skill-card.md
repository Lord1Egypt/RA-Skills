## Description:

Data-SignalDetector analyzes descriptions of datasets, model behavior, and training metrics for indicators of AI model poisoning or backdoors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[3mper0rr](https://clawhub.ai/user/3mper0rr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security reviewers, and AI supply chain analysts use this skill to triage user-provided descriptions of datasets, model behaviors, or training metrics for signs of backdoors, Trojans, and data poisoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A poisoning or backdoor assessment may be incomplete when the supplied model, dataset, or metric description is incomplete or misleading.

Mitigation: Treat the output as triage guidance and confirm findings with independent tests such as Neural Cleanse, activation clustering, or targeted trigger evaluation.

Risk: The skill steers the assistant into a specialized security-analysis format, which could overstate compromise if explicit indicators are absent.

Mitigation: Require detected indicators to be grounded in the provided data and preserve the skill constraint against unsupported assumptions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/3mper0rr/skills/data-signaldetector)
- [Artifact skill definition](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown-style analysis with labeled status, indicators, attack hypothesis, and verification action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only the logical and statistical patterns provided by the user; no code execution, file access, credentials, or external service calls are requested.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
