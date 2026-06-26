## Description: <br>
Submit products to CurlShip, the bot-friendly SaaS directory. One curl command to list your product with OG tag scraping, badge-based dofollow links, and tier upgrades. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MarcinDudekDev](https://clawhub.ai/user/MarcinDudekDev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, founders, and agents use this skill to submit a product or SaaS URL to the CurlShip directory, inspect active listings, request a paid tier checkout URL, and retrieve badge HTML for a dofollow link. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to submit a product URL and contact email to CurlShip for a public listing. <br>
Mitigation: Confirm the exact URL and email with the user before submission. <br>
Risk: The upgrade flow can return a checkout URL for a paid listing tier. <br>
Mitigation: Confirm the requested tier with the user and leave payment completion to the user. <br>
Risk: The skill may provide badge HTML intended for placement on the user's website. <br>
Mitigation: Review badge HTML before making website changes. <br>


## Reference(s): <br>
- [CurlShip homepage](https://curlship.com) <br>
- [CurlShip pricing](https://curlship.com/pricing) <br>
- [CurlShip submit endpoint](https://curlship.com/api/submit) <br>
- [CurlShip listings endpoint](https://curlship.com/api/listings) <br>
- [ClawHub skill page](https://clawhub.ai/MarcinDudekDev/curlship) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, JSON, guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces guidance for external HTTPS API calls; it does not require credentials or modify local files.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
