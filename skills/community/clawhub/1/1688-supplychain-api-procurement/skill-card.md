## Description:

Supports 1688 supply-chain procurement workflows by starting a procurement inquiry, returning an instanceId, and querying instance data by instanceId with file-mode output for large JSON results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1688aiinfra](https://clawhub.ai/user/1688aiinfra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to initiate 1688 procurement inquiries from complete purchasing requirements and later retrieve inquiry instance data without placing large JSON payloads into the model context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs API credentials and sends procurement text, inquiry questions, session metadata, and optional images to 1688 services.

Mitigation: Review credential handling before installation and submit only procurement content and images intended for 1688 processing.

Risk: Image handling accepts local paths and remote image URLs, which can upload or fetch content outside the immediate prompt.

Mitigation: Use only trusted local image paths and avoid remote image URLs unless the target is trusted.

Risk: Successful commands report usage metadata without a documented opt-out in the evidence.

Mitigation: Review the usage reporting behavior and organizational telemetry requirements before deployment.

Risk: Instance data can be large enough to overload or expose excessive detail in model context if returned inline.

Mitigation: Use the documented file-mode query path and stream the result file instead of summarizing or embedding the JSON in chat.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1688aiinfra/skills/1688-supplychain-api-procurement)
- [1688 skills gateway endpoint](https://skills-gateway.1688.com)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Files]

**Output Format:** [Raw JSON passthrough for inquiry creation and streamed JSON file output for instance data queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Inquiry creation returns only instanceId; instance data queries must use file output to avoid large model-context payloads.]

## Skill Version(s):

0.0.6 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
