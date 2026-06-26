## Description: <br>
Grade Amazon product listing quality from an ASIN with a 0-100 score, a seven-dimension breakdown, and improvement suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbeihanda](https://clawhub.ai/user/linbeihanda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate Amazon product listing quality, identify strong and weak listing dimensions, and prioritize improvements for title, bullets, reviews, sales signals, BSR, and badges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Each run sends the user's CLAW_KEY and Amazon product URL to the configured external scraping API. <br>
Mitigation: Use only a trusted HTTPS CLAW_API_BASE value supplied with the key, keep the .env file private, and rotate the key if it may have been exposed. <br>
Risk: Listing grades depend on parsed Amazon page data returned by the configured service and may be incomplete or stale. <br>
Mitigation: Review the returned title, listing fields, score breakdown, and suggestions before using the grade for business decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbeihanda/amazon-listing-judge) <br>
- [CLAW key provider](https://claw-school.com) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, shell commands, guidance] <br>
**Output Format:** [JSON result with score, grade, per-dimension breakdown, and suggestions; agents may present it as a structured report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ASIN plus CLAW_KEY and CLAW_API_BASE credentials for the configured scraping service.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
