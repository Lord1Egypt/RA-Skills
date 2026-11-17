## Description:

Parses a free-text address blob (supplier email, Google Maps result, business card) into structured fields (street, postal code, city, state, country, contact, phone) via an LLM chat-completions call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to add a paste-a-blob address parsing and autofill workflow to forms with separate address, contact, and phone fields. It guides prompt design, API request shape, defensive JSON parsing, server-side limits, non-destructive client merges, and tests for ambiguous or multilingual input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pasted address, contact, and phone data may be sent to the configured LLM provider.

Mitigation: Confirm the application is permitted to share that data with the provider before installation or deployment.

Risk: Client-side exposure of LLM credentials would allow unauthorized API use.

Mitigation: Keep API keys server-side and use bearer tokens only from server-side configuration.

Risk: Locale or language normalization may not match the product's expected country or address format.

Mitigation: Adjust the country and language normalization rules to the target product's locale before release.

Risk: LLM output can be malformed, overlong, or overconfident for ambiguous input.

Mitigation: Validate JSON against the expected schema, enforce server-side length limits, preserve empty-string-not-guess behavior, and surface low confidence for manual review.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Code, Configuration]

**Output Format:** [Markdown with JSON and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance for schema design, LLM chat-completions requests, defensive response parsing, field-length enforcement, non-destructive form merging, and test scenarios.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter metadata and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
