## Description:

Gets AI-generated markdown descriptions for points of interest using POI IDs from web search location results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to enrich local search workflows with narrative, travel-guide-style descriptions for businesses and places. It is intended for POI IDs previously returned by web search location results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick start uses an unpinned npm payment helper that may change over time and executes locally.

Mitigation: Use a pinned, reviewed version of the payment helper and run it in a least-privileged environment.

Risk: Automatic x402 payments can sign and retry paid requests without enough transaction review.

Mitigation: Require explicit transaction review or spending limits before enabling automatic payment flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sprintmint/skills/cpbox-local-descriptions)
- [CPBox API provider](https://www.cpbox.io)
- [CPPay facilitator](https://www.cppay.finance)
- [Local descriptions endpoint](https://www.cpbox.io/api/x402/local-descriptions)
- [Web search locations endpoint example](https://www.cpbox.io/api/x402/web-search?q=restaurants+san+francisco&result_filter=locations)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Guidance]

**Output Format:** [Markdown descriptions returned in JSON API responses, with usage guidance and curl or npx command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts 1-20 opaque POI IDs that are valid for approximately 8 hours; descriptions may be null when unavailable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
