## Description:

Company profiles and recent SEC filings from EDGAR via Edgrapi.com. Resolve a US-listed ticker to its CIK, industry, fiscal-year end, and exchange, and list its recent 10-K / 10-Q / 8-K filings with document links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperandbeyond23-gif](https://clawhub.ai/user/paperandbeyond23-gif)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill when they need an agent to look up US-listed company profile details and recent SEC filing history for a specific ticker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker lookups are sent to Edgrapi for SEC filing retrieval.

Mitigation: Use the skill only for intended company filing lookups and avoid including sensitive non-public context with requests.

Risk: EDGRAPI_KEY is used for authentication.

Mitigation: Keep the key in the environment variable and do not reveal it in prompts, outputs, or logs.

Risk: Each Edgrapi API call consumes one credit.

Mitigation: Activate the skill only for genuine lookup requests and use bounded filing limits.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/paperandbeyond23-gif/edgrapi-skills/tree/main/skills/edgrapi-filings)
- [Edgrapi](https://edgrapi.com)
- [Edgrapi app](https://edgrapi.com/app)
- [Edgrapi pricing](https://edgrapi.com/pricing)
- [ClawHub skill page](https://clawhub.ai/paperandbeyond23-gif/skills/edgrapi-filings)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with JSON-like lookup results from company and filings tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires EDGRAPI_KEY; each Edgrapi request consumes one credit.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
