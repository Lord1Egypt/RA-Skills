## Description:

Generates client-ready, single-page HTML proposals for freelancers, solo consultants, and small studios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoquanlong](https://clawhub.ai/user/guoquanlong)

### License/Terms of Use:

MIT-0

## Use Case:

External freelancers, solo consultants, and small studios use this skill to turn a short client brief into a polished proposal, quote, or pitch document. It helps an agent collect proposal fields, prepare structured copy, and render a self-contained HTML file for preview, printing, or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated client-facing HTML can include unsanitized active content if untrusted markup is passed through the fields JSON.

Mitigation: Avoid feeding untrusted HTML or client-provided markup into fields, and review every generated HTML file before sharing it.

Risk: The optional contact watermark can expose default or unintended contact branding in shared previews.

Mitigation: Replace or remove the default contact values and set SHOW_CONTACT_WATERMARK to false unless the watermark is intentional.

## Reference(s):

- [Proposal Structure Reference](references/proposal-structure.md)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with JSON field data, shell commands, and generated single-page HTML]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline deterministic rendering; generated HTML should be reviewed before sharing.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
