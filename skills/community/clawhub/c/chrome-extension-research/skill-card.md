## Description:

Compare Chrome extensions using Crawlora's live store listings and stored adoption, publisher, permission, and privacy history for shortlists, market comparisons, and investigating observed changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and extension evaluators use this skill to shortlist and compare Chrome extensions by store listings, observed adoption and publisher changes, declared permissions, privacy disclosures, and sampled reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and the API key are sent to Crawlora as an external service.

Mitigation: Use a dedicated API key and avoid private or sensitive text in extension IDs, search terms, filters, and other query values.

Risk: Store disclosures, ratings, and sampled reviews may be mistaken for proof of extension safety or typical behavior.

Mitigation: Label disclosures as developer claims, date observations, and seek independent code or runtime review before drawing safety conclusions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/crawlora-org/skills/chrome-extension-research)
- [Crawlora endpoint reference](reference/endpoints.md)
- [Chrome extension permission definitions](https://developer.chrome.com/docs/extensions/develop/concepts/declare-permissions)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown comparison with source links and dated observations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Separates observed facts from developer claims and identifies missing evidence.]

## Skill Version(s):

1.0.11 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
