## Description:

Search G2, the B2B software review site, read a full product profile with pricing and features, and pull faceted reviews with exact per-star counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scavio-ai](https://clawhub.ai/user/scavio-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to query Scavio's G2 endpoints for B2B software search, product profiles, pricing, alternatives, and review facets for product research, competitive intelligence, and voice-of-customer analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: G2 search terms, product identifiers, filters, and the Scavio API key are sent to Scavio when API calls are made.

Mitigation: Confirm that the requested data can be shared with Scavio before calling the API, and keep the API key in an environment variable or secret store.

Risk: Each G2 endpoint call spends Scavio credits, and multi-page review pulls can become expensive.

Mitigation: State the planned credit cost before calls, avoid looping over product profiles, and limit pagination to the user's explicit need.

Risk: Filtered review calls that return zero results can be ambiguous, and product profile calls do not include review text.

Mitigation: Re-check filtered zero-result findings without filters before reporting conclusions, and use the reviews endpoint for customer sentiment.

Risk: Optional SDK installation introduces normal package-management and dependency-review concerns.

Mitigation: Prefer direct HTTPS calls when the SDK is unnecessary, or install optional packages in a virtual environment with reviewed dependency versions.

## Reference(s):

- [Scavio G2 Search Documentation](https://scavio.dev/docs/g2-search)
- [Scavio Rate Limits](https://scavio.dev/docs/rate-limits)
- [ClawHub Skill Listing](https://clawhub.ai/scavio-ai/skills/g2-software-reviews)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API calls, JSON]

**Output Format:** [Markdown guidance with inline shell and code examples, plus structured JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SCAVIO_API_KEY; Scavio G2 endpoints cost 5 credits per request.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
