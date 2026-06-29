## Description: <br>
Extracts customer reviews from e-commerce product or reviews pages, including reviewer, rating, date, title, body, verified purchase status, and helpful vote fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to collect publicly visible customer-review data from product pages for feedback analysis, ratings review, or downstream sentiment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads visible review content from pages the user opens and may keep a small local notes file about unusual scraping issues. <br>
Mitigation: Use it only on pages where review collection is permitted by site terms, privacy expectations, and organizational rules; review local notes if unusual scraping issues occur. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/browseract-cli/ecommerce-reviews-skill) <br>
- [Publisher profile](https://clawhub.ai/user/browseract-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown guidance with shell commands that produce JSON review records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review extraction includes reviewer, rating, date, title, body, verified purchase status, helpful votes, and count fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
