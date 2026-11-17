## Description:

Fapi Reddit lets an agent use fapi.uk's Reddit REST API to look up users, subreddit posts, search results, and post details from natural-language requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huojiecs110](https://clawhub.ai/user/huojiecs110)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query Reddit content through fapi.uk by asking an agent for user activity, subreddit posts, search results, or post details without manually assembling REST parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose paid-service credentials if users paste API keys or auth tokens into chat or logs.

Mitigation: Use secure configuration storage for a narrowly scoped, revocable fapi.uk API key, avoid sharing credentials in chat, and rotate any credential that was already exposed.

Risk: Requests to fapi.uk can spend account credits.

Mitigation: Confirm the account balance and expected cost before live use, and stop when credits are insufficient.

## Reference(s):

- [Fapi Reddit ClawHub page](https://clawhub.ai/huojiecs110/skills/fapi-reddit)
- [huojiecs110 ClawHub profile](https://clawhub.ai/user/huojiecs110)
- [fapi.uk](https://fapi.uk)
- [fapi.uk documentation](https://utools.readme.io)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration guidance]

**Output Format:** [Markdown or plain text summaries, with shell commands for setup and JSON only when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a fapi.uk API key for live requests and may spend account credits when API calls are made.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
