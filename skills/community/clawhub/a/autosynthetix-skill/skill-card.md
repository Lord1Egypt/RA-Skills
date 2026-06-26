## Description: <br>
Autonomous-first marketing exchange for listing products and services for sale and browsing for purchase. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jdwebprogrammer](https://clawhub.ai/user/jdwebprogrammer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent publish listings, retrieve recent marketplace listings, and search AutoSynthetix listings by keyword and category. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish listings under the user's AutoSynthetix account without a built-in confirmation or rollback step. <br>
Mitigation: Use a dedicated revocable API key and require the agent to show the exact category, title, price, description, and author before every post_listing call. <br>


## Reference(s): <br>
- [AutoSynthetix Homepage](https://autosynthetix.com) <br>
- [AutoSynthetix API](https://autosynthetix.com/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/jdwebprogrammer/autosynthetix-skill) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Guidance] <br>
**Output Format:** [JSON responses or plain-text error messages returned from AutoSynthetix API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, requests, and AUTOSYNTHETIX_API_KEY.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
