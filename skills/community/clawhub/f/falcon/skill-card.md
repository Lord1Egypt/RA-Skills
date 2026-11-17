## Description:

Search, read, and interact with Twitter/X via TwexAPI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bubblyjove](https://clawhub.ai/user/bubblyjove)

### License/Terms of Use:


## Use Case:

Developers and external users can use Falcon to search Twitter/X, read profiles and tweets, check trends, and perform account actions through TwexAPI-backed shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write and engagement commands delegate a reusable Twitter/X session cookie to TwexAPI for account-changing actions.

Mitigation: Use only with an account and cookie you are comfortable exposing to TwexAPI, and prefer a version that supports scoped OAuth credentials.

Risk: Posting, following, liking, retweeting, bookmarking, and similar actions can change the connected Twitter/X account state.

Mitigation: Confirm intent before every write or engagement command, and prefer a dry-run or in-tool confirmation flow before execution.

Risk: The artifact includes broad local Bash allowlist entries.

Mitigation: Restrict local Bash permissions to the specific Falcon commands required for the deployment.

## Reference(s):

- [Falcon ClawHub skill page](https://clawhub.ai/bubblyjove/skills/falcon)
- [TwexAPI service endpoint](https://api.twexapi.io)
- [Publisher profile](https://clawhub.ai/user/bubblyjove)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, TWEXAPI_KEY, and TWITTER_COOKIE for write or engagement actions.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
