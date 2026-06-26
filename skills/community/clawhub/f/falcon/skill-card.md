## Description: <br>
Search, read, and interact with Twitter/X via TwexAPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BubblyJove](https://clawhub.ai/user/BubblyJove) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use Falcon to search, read, and manage Twitter/X content through TwexAPI-backed shell commands. It supports profile and tweet lookup, search workflows, trends, posting, and account engagement actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a Twitter/X session cookie to post content or change account state. <br>
Mitigation: Use read-only mode with TWITTER_COOKIE unset unless posting or engagement is intentionally required. <br>
Risk: Posting, liking, retweeting, bookmarking, following, or unfollowing can create public or account-visible effects. <br>
Mitigation: Require explicit user confirmation before every write or engagement command. <br>
Risk: The TwexAPI bearer token and Twitter/X cookie grant access to external account data and actions. <br>
Mitigation: Install only when the publisher and TwexAPI are trusted with the represented Twitter/X account. <br>


## Reference(s): <br>
- [Falcon on ClawHub](https://clawhub.ai/BubblyJove/falcon) <br>
- [TwexAPI endpoint](https://api.twexapi.io) <br>
- [TwitterXAPI documentation](https://docs.twitterxapi.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, JSON, configuration, guidance] <br>
**Output Format:** [Shell command guidance and JSON API responses formatted through jq] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, TWEXAPI_KEY, and TWITTER_COOKIE for write or engagement commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
