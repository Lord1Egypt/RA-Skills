## Description:

Monitor Amazon product reviews by ASIN, analyze ratings and sentiment, identify issues, and draft seller response text for negative feedback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avmw2025](https://clawhub.ai/user/avmw2025)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce operators use this skill to monitor product reviews by ASIN, summarize rating and sentiment patterns, identify negative themes, and draft professional seller responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can be steered to make arbitrary HTTPS requests and lacks basic limits on scraping volume.

Mitigation: Review before execution, use only trusted ASIN and marketplace values, keep page counts low, and add marketplace allowlisting, ASIN validation, page limits, response-size limits, and redirect validation.

Risk: The skill scrapes live Amazon pages and saves review data locally.

Mitigation: Make scraping and local report storage clear to users, and manage generated review reports appropriately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avmw2025/skills/amazon-review-monitor)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Terminal text with saved JSON report files and seller response drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Saves review reports locally under the skill reports directory when analysis succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
