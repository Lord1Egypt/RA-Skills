## Description:

Drawing Cleaner cleans raw Markdown drawing text by filtering noise such as axis labels, title-block fields, dimension-only lines, and garbled fragments, then classifies retained content into drawing information, design notes, component identifiers, reinforcement details, material strengths, elevations, construction details, and other review items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lialia691691-alt](https://clawhub.ai/user/lialia691691-alt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, construction documentation teams, and quantity-surveying workflows use this skill to turn raw drawing-text Markdown extracts into cleaner categorized Markdown before downstream bill-of-quantities review or generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The cleaner writes Markdown output to a user-selected or derived path.

Mitigation: Review the input and output paths before running the script.

Risk: Cleaned drawing content may still contain project-specific or sensitive construction data.

Mitigation: Treat cleaned content as quoted project data before sharing it with downstream AI tools or external systems.

Risk: An unusually low or high cleaning rate can indicate under-filtering or over-filtering of drawing content.

Mitigation: Review the generated noise-rate statistics and manually inspect retained categories when the rate is outside the expected range.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lialia691691-alt/skills/drawing-cleaner)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown files and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The cleaner reads selected Markdown input files and writes categorized, deduplicated Markdown output with line-count and noise-rate statistics.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
