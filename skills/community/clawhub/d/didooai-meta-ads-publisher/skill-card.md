## Description: <br>
[Didoo AI] Executes Meta Ads campaign management tasks, including creating campaigns, making changes, pausing or activating campaigns, changing budgets, and duplicating campaigns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elias-didoo](https://clawhub.ai/user/elias-didoo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and operators use this skill to guide an agent through Meta Ads campaign creation, duplication, budget changes, status changes, campaign listing, and performance review. It is intended for accounts where the user has supplied Meta Marketing API credentials and can review spend-affecting actions before activation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make spend-affecting changes to a Meta Ads account. <br>
Mitigation: Use a least-privileged token for the intended ad account and require explicit user confirmation of the ad account, object IDs, budget, status, and exact change before create, duplicate, budget, pause, or activate actions. <br>
Risk: Campaigns or duplicated campaigns could be activated before review. <br>
Mitigation: Keep new campaigns paused until human review confirms targeting, creative, budget, tracking, and bid strategy. <br>
Risk: The skill requires sensitive Meta Marketing API credentials. <br>
Mitigation: Store credentials only in the platform secret manager, never expose tokens in conversation or logs, and use the token only for Meta Marketing API calls. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/elias-didoo/didooai-meta-ads-publisher) <br>
- [Meta Graph API v21.0 Endpoint](https://graph.facebook.com/v21.0/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, API calls, configuration] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Meta access token and ad account ID; recommends creating campaigns paused until review.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
