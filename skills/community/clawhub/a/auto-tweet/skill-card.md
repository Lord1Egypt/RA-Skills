## Description: <br>
Post, search, like, retweet, bookmark, and manage a Twitter/X account via a local twikit-based API server on port 19816. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chatgptnexus](https://clawhub.ai/user/chatgptnexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate a Twitter/X account from an agent through a local API for posting, searching, timeline review, reactions, bookmarks, direct messages, follows, and scheduled tweets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local server can exercise substantial control over a live Twitter/X account. <br>
Mitigation: Use a dedicated account where possible and require explicit human confirmation before posts, DMs, deletes, follows, retweets, or scheduled tweets. <br>
Risk: Account credentials and session cookies are stored locally. <br>
Mitigation: Protect config.json and cookies.json, restrict local file access, and remove credentials when the skill is no longer needed. <br>
Risk: Weak safeguards or accidental local exposure could allow unintended account actions. <br>
Mitigation: Keep the server bound to 127.0.0.1, stop it when finished, and keep conservative rate limits enabled. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/chatgptnexus/auto-tweet) <br>
- [Twikit project](https://github.com/d60/twikit) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local service returns JSON responses from Twitter/X automation endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
