## Description:

Searches for images and returns result titles, source URLs, thumbnails, SafeSearch filtering, and up to 200 results per request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to query paid CPBox image search through x402 and retrieve image metadata for galleries, mood boards, visual research, or content enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic x402 payment signing can spend funds or expose payment credentials beyond the operator's intended scope.

Mitigation: Run with limited payment credentials and spending caps, and require confirmation before automatic signing.

Risk: The documented npx command runs the x402 payment helper without a pinned package version.

Mitigation: Use a pinned, reviewed version of @springmint/x402-payment before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintmint/skills/cpbox-images-search)
- [CPBox API provider](https://www.cpbox.io)
- [CPBox images search endpoint](https://www.cpbox.io/api/x402/images-search)
- [CPPay facilitator](https://www.cppay.finance)

## Skill Output:

**Output Type(s):** [JSON, shell commands, guidance]

**Output Format:** [Markdown instructions with HTTP and bash examples; API responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image results can include titles, page URLs, source domains, thumbnails, original image URLs, dimensions, relevance confidence, and SafeSearch or offensive-content indicators.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
