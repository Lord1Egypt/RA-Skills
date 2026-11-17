## Description:

Validates Chinese ID numbers and extracts region code, birth date, and gender information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill as a local reference utility to check Chinese ID number format, checksum, birth date, gender, and region-code fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive Chinese ID numbers, creating privacy risk if real identifiers are logged, submitted, or retained unnecessarily.

Mitigation: Use it locally, mask raw IDs where possible, collect only with lawful need and consent, and retain identifiers minimally.

Risk: Validation gaps could mislead identity or age-verification workflows because the evidence reports numeric and region validation issues.

Mitigation: Do not rely on this skill as the sole identity or age-verification control until numeric and region validation are fixed and independently reviewed.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No external dependencies; the included script emits JSON for validation results.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
