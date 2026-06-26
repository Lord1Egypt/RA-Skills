## Description: <br>
Fetches Amazon product reviews through the Reveyes API, including rating distribution, star filtering, and critical review summaries across supported marketplaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhuojiuya](https://clawhub.ai/user/zhuojiuya) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce analysts, and agents use this skill to fetch Amazon product review data by ASIN across supported marketplaces and summarize ratings, review volume, and critical feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a REVEYES_API_KEY and calls the Reveyes API. <br>
Mitigation: Store the API key only in environment or secret configuration, avoid committing it to files, and rotate it if exposed. <br>
Risk: Review fetching consumes Reveyes credits per page. <br>
Mitigation: Keep page counts small unless broader collection is necessary, and confirm credit availability before large requests. <br>
Risk: Fetched review results depend on the requested ASIN, marketplace, page count, star filter, and external service availability. <br>
Mitigation: Treat outputs as a collected sample for the requested parameters and verify important business conclusions against additional sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhuojiuya/amazon-review) <br>
- [Reveyes official site](https://www.reveyes.cn) <br>
- [Reveyes Python SDK](https://pypi.org/project/reveyes/) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zhuojiuya) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries and JSON review data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes ASIN, marketplace, total reviews, average rating, rating distribution, top critical reviews, and credits used when the API call succeeds.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact files report 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
