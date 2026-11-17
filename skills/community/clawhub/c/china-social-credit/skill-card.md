## Description:

Validates and parses Chinese Unified Social Credit Codes (统一社会信用代码) offline, including checksum, registration authority, organization type, and registered location according to GB 32100-2015.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and operations teams use this skill to validate Chinese business or organization identification codes during contract review, supplier checks, or enterprise data entry. It reports format, checksum, registration authority, organization type, registered location, and likely input errors without querying live registries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A valid checksum may be mistaken for proof that an organization exists or is in good standing.

Mitigation: Use the result as offline format validation only and confirm legal or operational status through an authoritative registry when needed.

Risk: Historical or non-standard license numbers may be outside the GB 32100-2015 parsing assumptions.

Mitigation: Treat unsupported formats as out of scope and verify them through original documents or an official source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/china-social-credit)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style structured text with validation status, parsed fields, error reasons, and suggestions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline; no network calls or API keys required; validates format and checksum only, not company existence or good standing.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
