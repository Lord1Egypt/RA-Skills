## Description: <br>
Enables an agent to use fapi.uk Twitter/X REST APIs from natural-language requests for posting, search, interactions, user management, communities, Grok tools, media upload, and notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huojiecs110](https://clawhub.ai/user/huojiecs110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate Twitter/X workflows through fapi.uk, including publishing, searching, media upload, account interactions, community queries, and Grok-related actions from a conversational agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for powerful Twitter/X account credentials and fapi.uk API credentials. <br>
Mitigation: Use a low-risk or dedicated Twitter/X account and store credentials only through a secure config or secret mechanism; do not paste real tokens into chat. <br>
Risk: The skill can perform account-changing actions such as posts, replies, follows, unfollows, blocks, unlocks, bookmarks, retweets, and likes. <br>
Mitigation: Require explicit user confirmation before any post, reply, follow, unfollow, block, unlock, or other account-changing action. <br>
Risk: API calls consume fapi.uk account credits, and some actions may have extra cost. <br>
Mitigation: Check account balance before every action, stop when credits are insufficient, and require explicit approval before any paid or credit-consuming action. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/huojiecs110/fapi-twitter) <br>
- [fapi.uk](https://fapi.uk) <br>
- [fapi.uk API documentation](https://utools.readme.io/reference) <br>


## Skill Output: <br>
**Output Type(s):** [text, API calls, shell commands, configuration guidance] <br>
**Output Format:** [Natural-language summaries with setup commands and optional raw API data on request] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Checks fapi.uk account balance before actions and stops when credits are insufficient.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
