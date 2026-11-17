## Description:

Post, search, like, retweet, bookmark, and manage a Twitter/X account via a local twikit-based API server on port 19816.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chatgptnexus](https://clawhub.ai/user/chatgptnexus)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to operate a local Twitter/X automation server for posting, searching, timeline review, engagement actions, direct messages, and account-management workflows through an agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill exposes powerful Twitter/X account actions through an unauthenticated local API.

Mitigation: Run only on a trusted machine, keep the service bound to localhost, do not expose the port, and add API authentication before real account use.

Risk: Twitter/X credentials and session cookies are stored in local files.

Mitigation: Treat config.json and cookies.json like account passwords, restrict file permissions, and avoid sharing or committing those files.

Risk: Account-changing actions such as tweeting, deleting, following, unfollowing, liking, retweeting, bookmarking, and sending DMs can affect a real account.

Mitigation: Require explicit confirmation for each account-changing action and use conservative rate limits.

## Reference(s):

- [twikit](https://github.com/d60/twikit)
- [Auto Tweet Publish on ClawHub](https://clawhub.ai/chatgptnexus/skills/auto-tweet)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local HTTP requests and operational guidance for a Twitter/X automation server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
