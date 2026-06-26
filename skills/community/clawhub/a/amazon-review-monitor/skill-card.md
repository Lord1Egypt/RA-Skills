## Description: <br>
Monitor Amazon product reviews by ASIN, analyze rating distribution and sentiment, identify negative themes, and draft seller response text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avmw2025](https://clawhub.ai/user/avmw2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
E-commerce sellers and support teams use this skill to review recent Amazon customer feedback for a product ASIN, spot negative themes, and prepare draft seller responses for manual review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill contacts Amazon and scrapes public review pages for a user-provided ASIN. <br>
Mitigation: Use reasonable page counts and confirm the activity fits the user's marketplace, account, and site-policy constraints before repeated runs. <br>
Risk: Saved reports contain scraped review text and generated analysis that may be sensitive business data. <br>
Mitigation: Store reports in an appropriate local workspace, limit sharing, and delete reports when they are no longer needed. <br>
Risk: Seller response drafts may be incomplete, inaccurate, or unsuitable for direct posting. <br>
Mitigation: Manually review and edit every drafted response before publishing it or sending it to customers. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/avmw2025/amazon-review-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands] <br>
**Output Format:** [Console text with local JSON report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Saves scraped review text, sentiment analysis, rating summaries, and draft responses to a local reports folder when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
