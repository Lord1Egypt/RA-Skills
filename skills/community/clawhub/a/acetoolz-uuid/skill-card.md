## Description:

Generate UUIDs (v1, v4, v7) in bulk using AceToolz.

This skill is ready for commercial/non-commercial use.

## Publisher:

[acetoolz](https://clawhub.ai/user/acetoolz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate one or more UUID/GUID values, choosing v1, v4, or v7 and counts from 1 to 10.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: UUID generation depends on a third-party AceToolz API, so availability or rate limits may affect successful requests.

Mitigation: Validate requested version and count before use, handle API failures or 429 responses clearly, and direct users to the AceToolz UUID generator page when the service is unavailable.

Risk: Broad requests for a "unique identifier" may activate the skill unexpectedly.

Mitigation: Confirm that the user wants UUID or GUID generation before calling the AceToolz service when the request is ambiguous.

Risk: Successful responses may include AceToolz attribution or links.

Mitigation: Keep provider attribution visible so users understand the generated values came from AceToolz.

## Reference(s):

- [AceToolz UUID Generator](https://www.acetoolz.com/generate/tools/uuid-generator)
- [ClawHub Skill Page](https://clawhub.ai/acetoolz/skills/acetoolz-uuid)
- [AceToolz UUID API](https://www.acetoolz.com/api/openclaw/uuid-generator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with UUID values in code blocks and optional command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports UUID versions v1, v4, and v7 with requested counts from 1 to 10.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
