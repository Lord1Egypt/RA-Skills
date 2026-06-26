## Description: <br>
Fetches the latest original e-commerce news from Ebrun by matching a user's channel or topic request and returning recent article details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ebrun-developer](https://clawhub.ai/user/ebrun-developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to retrieve current Ebrun e-commerce articles for channel-specific news browsing, briefings, or automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound HTTPS requests to Ebrun and occasional version-check requests to GitHub or Gitee. <br>
Mitigation: Use it only in environments that permit those network destinations, or review and disable the update-check step for strict no-egress deployments. <br>
Risk: The version-check flow writes a small temporary cache. <br>
Mitigation: Review cache handling before use in environments with strict no-cache or retention requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ebrun-developer/ebrun-original-news) <br>
- [Publisher profile](https://clawhub.ai/user/ebrun-developer) <br>
- [Ebrun website](https://www.ebrun.com/) <br>
- [API reference](references/api-reference.md) <br>
- [Channel list](references/channel-list.json) <br>
- [Version metadata](references/version.json) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown news summaries or JSON article arrays with titles, authors, summaries, publish times, and HTTPS source links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 10 latest articles by default and may include a version-update notice when an update is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and references/version.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
