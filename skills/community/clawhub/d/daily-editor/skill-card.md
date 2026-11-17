## Description:

Runs a private editorial workflow that turns daily information into an A4 portrait PDF brief with customizable sections, restrained editorial judgment, safer phrasing, and source links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[igloomatics](https://clawhub.ai/user/igloomatics)

### License/Terms of Use:

MIT-0

## Use Case:

External users and employees use this skill to create a concise, calm daily digest as a single A4 portrait PDF. It is intended for customized news, domain, product, or personal-note sections with visible source attribution and an optional recurring delivery workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring runs can generate or deliver briefs at the wrong cadence, time, timezone, or destination if scheduling details are ambiguous.

Mitigation: Confirm cadence, delivery time, timezone, output path, and whether draft preview is required before enabling recurring generation.

Risk: Daily briefs may unintentionally overstate sensitive or controversial source material.

Mitigation: Use the skill's calm editorial tone, high-level treatment of sensitive topics, and source-link requirements to preserve factual context without graphic or sensational detail.

## Reference(s):

- [PDF Target](pdf-target.md)
- [Reference](reference.md)
- [Scheduling](schedule.md)
- [A4 PDF Templates](templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance, Files]

**Output Format:** [Markdown guidance with optional HTML/CSS render source, shell commands, and PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a single-file A4 portrait PDF by default; may provide scheduling instructions for recurring local generation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
