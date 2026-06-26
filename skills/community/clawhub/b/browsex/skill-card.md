## Description: <br>
browsex helps agents use OpenClaw's browser tool to read X/Twitter content and, with an authenticated account, post, like, repost, reply, search, or follow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[coding-commits](https://clawhub.ai/user/coding-commits) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to control an X/Twitter browser session from an agent workflow. It supports read-only browsing without login and account-changing actions when the user has authenticated the browser profile. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An authenticated browser session can make public or account-changing actions on X/Twitter. <br>
Mitigation: Use a separate browser profile where possible and require explicit approval before posts, replies, reposts, likes, and follows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/coding-commits/browsex) <br>
- [Publisher profile](https://clawhub.ai/user/coding-commits) <br>
- [X login](https://x.com/login) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with browser action command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires fresh browser snapshots for current element references and user confirmation before posting.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
