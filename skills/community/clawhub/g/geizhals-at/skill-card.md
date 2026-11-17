## Description:

Search Geizhals.at (Austria) with HTTP-only autocomplete and detail-page parsing for quick, best-effort price checks without browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rolandkakonyi](https://clawhub.ai/user/rolandkakonyi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to search Geizhals.at product candidates and retrieve price-oriented result records, including cheapest observed price, shop, offer count, confidence, source, and detail URL.

### Deployment Geography for Use:

Global, with Austria-focused Geizhals.at results.

## Known Risks and Mitigations:

Risk: Returned search data may steer the scraper to request non-Geizhals URLs and cache the responses.

Mitigation: Review before installing in environments with private-network or metadata-service access; prefer a version that allowlists https://geizhals.at, accepts only relative Geizhals paths, validates redirects, and makes cache behavior clear or optional.

Risk: The unofficial HTTP scraper can return incomplete or stale price data when Geizhals page structure, rate limiting, or autocomplete behavior changes.

Mitigation: Treat price output as best-effort, inspect price_confidence and price_source, keep request volume low, and verify important purchases against the linked detail page.

## Reference(s):

- [Geizhals.at](https://geizhals.at)
- [ClawHub skill page](https://clawhub.ai/rolandkakonyi/skills/geizhals-at)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [JSON records or plain-text price summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Records include schema_version, name, detail_url, min_price_eur, shop, offer_count, price_confidence, price_source, and error.]

## Skill Version(s):

0.1.1 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
