## Description:

This skill turns a CSV product list into consistent commercial product images, with concurrency, retries, resumable runs, cost limits, and a review contact sheet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dlazyai](https://clawhub.ai/user/dlazyai)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce teams can use this skill to generate a visually consistent set of product images from SKU records, then review sample outputs and the contact sheet before listing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because of reported purpose mismatch, cost-control and validation concerns; its analysis covered only part of the components.

Mitigation: Review the skill behavior and resolve the reported mismatches before installation; use a dry run and bounded sample batch, and inspect generated images and validation results before scaling up.

Risk: Product images and descriptions may be sent to the selected external image-generation provider, and the scan does not establish that partially inspected behavior is safe.

Mitigation: Confirm provider data handling is acceptable for the supplied materials and review the source before installation; avoid sending sensitive product assets until reviewed.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dlazyai/skills/batch-image)
- [Provider configuration and data flow](references/provider-cli.md)
- [Model flags](references/model-flags.md)
- [Platform image specifications](references/platform-specs.md)
- [Image quality check skill](https://github.com/dlazy-ai/ecommerce-skills/blob/main/skills/detect-task/skill.md)

## Skill Output:

**Output Type(s):** [Image files, CSV report, Contact sheet]

**Output Format:** [Generated product images plus a CSV run report and visual contact sheet]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are organized by SKU; review image fidelity and listing requirements before use.]

## Skill Version(s):

1.0.33 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
