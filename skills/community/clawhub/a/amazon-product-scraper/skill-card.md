## Description:

Scrapes Amazon product listing details such as title, price, sales signals, rankings, specifications, bullet descriptions, and variants, then generates a structured competitor analysis report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[denicmic-chung](https://clawhub.ai/user/denicmic-chung)

### License/Terms of Use:


## Use Case:

Developers, operators, and ecommerce analysts use this skill to collect product details from user-supplied Amazon ASINs or product URLs and produce a structured competitor analysis report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports are saved locally under memory/, which can retain sensitive notes or analysis added during use.

Mitigation: Avoid including sensitive internal notes unless local persistence is acceptable, and review retained report files according to the user's data-handling policy.

Risk: Amazon pages may block or vary browser scraping, which can lead to missing, stale, or incomplete product details.

Mitigation: Review the generated report against the live product page before relying on it for pricing, ranking, or competitive decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/denicmic-chung/skills/amazon-product-scraper)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown report with tables and structured analysis sections, also saved as a local markdown file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are saved under memory/ with the ASIN in the filename.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
