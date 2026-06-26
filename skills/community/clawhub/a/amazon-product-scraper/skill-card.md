## Description: <br>
Scrapes Amazon product listing details from a provided ASIN or product URL and generates a structured competitor analysis report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[denicmic-chung](https://clawhub.ai/user/denicmic-chung) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Amazon sellers, marketplace analysts, and agent users can provide an ASIN or Amazon product URL to collect product details and produce a competitor analysis report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports may retain product details in local memory after use. <br>
Mitigation: Delete saved reports that are no longer needed. <br>
Risk: Repeated automated browsing of Amazon pages could violate Amazon terms or rate limits. <br>
Mitigation: Use the skill only on product pages the user provides and avoid scraping patterns that exceed site terms or rate limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/denicmic-chung/amazon-product-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown] <br>
**Output Format:** [Markdown competitor analysis report, also saved as a local markdown file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes extracted product fields such as ASIN, title, price, ratings, rankings, specifications, variants, and analysis notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
