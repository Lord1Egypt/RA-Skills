## Description:

ClawFetch lets agents retrieve and process web data through fetch, JavaScript rendering, structured extraction, document parsing, domain, company, and research endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mssteuer](https://clawhub.ai/user/mssteuer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use ClawFetch to retrieve pages that need JavaScript rendering, extract structured information from supported sites, parse documents, check domains, enrich company profiles, and gather multi-source research for an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup example prints a wallet private key, which could expose funds if the key is retained in logs.

Mitigation: Remove private-key logging, store keys in protected storage, and replace any key that has appeared in logs before funding it.

Risk: Paid requests can spend USDC from the configured wallet, and submitted URLs, queries, and documents are shared with ClawFetch.

Mitigation: Use a dedicated wallet with a small balance and spending limit, and avoid submitting information that should not be shared with the service.

## Reference(s):

- [ClawFetch website](https://clawfetch.ai)
- [ClawFetch API](https://api.clawfetch.ai)
- [ClawHub skill release](https://clawhub.ai/mssteuer/skills/clawfetch-ai)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown, Guidance]

**Output Format:** [Plain text, structured JSON, or GitHub-Flavored Markdown, depending on endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Endpoint-specific results; scanned or image-only PDFs are not OCR-processed.]

## Skill Version(s):

2.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
