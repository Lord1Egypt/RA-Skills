## Description: <br>
Fetches Amazon product reviews for ASINs through the Reveyes API, including star distributions, critical review summaries, and review data across supported marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuojiuya](https://clawhub.ai/user/zhuojiuya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce analysts, and agents use this skill to fetch Amazon review data for ASINs, compare marketplace feedback, and summarize star distributions and critical reviews. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the Reveyes API key and ASIN query parameters to a third-party Reveyes API. <br>
Mitigation: Install only when use of Reveyes is intended, store REVEYES_API_KEY in an environment variable, and avoid submitting sensitive competitive-research queries unless that sharing is acceptable. <br>
Risk: Fetching review pages consumes Reveyes credits and may time out while a task continues running. <br>
Mitigation: Use the smallest page count that fits the task, monitor credit balance, and keep any returned task_id for follow-up when a timeout occurs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuojiuya/amazon-review-reveyes) <br>
- [Reveyes API website](https://www.reveyes.cn) <br>
- [Reveyes Python SDK](https://pypi.org/project/reveyes/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Markdown summary with optional JSON review data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires REVEYES_API_KEY and sends ASIN, marketplace, page count, and star filter values to the Reveyes API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
