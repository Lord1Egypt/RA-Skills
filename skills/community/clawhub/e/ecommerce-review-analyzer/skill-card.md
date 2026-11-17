## Description:

Analyzes Taobao, JD, and Pinduoduo ecommerce reviews, compares positive and negative feedback across products or stores, and produces review analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Ecommerce operators and analysts use this skill to gather product reviews from Taobao, JD, and Pinduoduo, summarize rating patterns and negative feedback, compare products or stores, and generate Word/PDF reports with improvement suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an authenticated browser session to gather ecommerce reviews.

Mitigation: Run it only in a scoped browser session and only with accounts and review data you are authorized to access.

Risk: Generated reports may include usernames, dates, and full comment text from ecommerce reviews.

Mitigation: Limit report distribution, remove unnecessary personal data, and store generated Word/PDF files according to your data handling policy.

Risk: The workflow depends on Python packages used for segmentation and document generation.

Mitigation: Install dependencies in a virtual environment and pin reviewed package versions before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/ecommerce-review-analyzer)
- [Publisher profile](https://clawhub.ai/user/tobewin)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser automation examples and generated Word/PDF report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include ecommerce review text, ratings, usernames, dates, platform names, store names, and product comparisons.]

## Skill Version(s):

1.0.7 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
