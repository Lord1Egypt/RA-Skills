## Description:

USE FOR query autocomplete/suggestions. Fast (<100ms). Returns suggested queries as user types. Supports rich suggestions with entity info. Typo-resilient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to call a paid CPBox autocomplete endpoint for search-as-you-type suggestions, RAG query refinement, entity detection, and typo-tolerant query cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic x402 payment calls can spend funds when the helper signs and retries paid requests.

Mitigation: Use a dedicated low-balance wallet or explicit payment limits before enabling automatic payment.

Risk: The unpinned npx payment helper may execute a package version that has not been reviewed.

Mitigation: Pin and review the x402 helper package version and run it in a restricted environment.

Risk: Autocomplete query text is sent to a paid third-party service.

Mitigation: Avoid sending sensitive queries unless the data-sharing and retention terms are acceptable for the use case.

## Reference(s):

- [CPBox Suggest API endpoint](https://www.cpbox.io/api/x402/suggest)
- [CPBox service](https://www.cpbox.io)
- [CPay facilitator](https://www.cppay.finance)
- [x402 payment setup](https://github.com/springmint/cpbox-skills#prerequisites)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with HTTP, bash, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces paid autocomplete request guidance and describes JSON suggestion responses; rich responses may include entity metadata.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
