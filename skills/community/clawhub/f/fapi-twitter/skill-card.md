## Description:

Enables agents to use fapi.uk's Twitter/X REST API through natural language for posting, search, engagement, user management, Grok, community, media, notification, and account workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huojiecs110](https://clawhub.ai/user/huojiecs110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to let an agent perform Twitter/X workflows through fapi.uk, including read-only search and account-changing actions such as posts, replies, follows, blocks, likes, bookmarks, media uploads, Grok interactions, and community operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to provide powerful Twitter/X account credentials and fapi.uk API keys.

Mitigation: Use a dedicated secret store when available, avoid pasting auth_token, ct0, cookies, or API keys into chat, and prefer narrowly scoped revocable credentials.

Risk: The skill enables account-changing Twitter/X actions and paid fapi.uk API usage through a third-party API.

Mitigation: Confirm every write action before execution, check account balance before requests, and understand that fapi.uk will receive credentials capable of account actions and paid usage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huojiecs110/skills/fapi-twitter)
- [fapi.uk](https://fapi.uk)
- [fapi.uk API reference](https://utools.readme.io/reference)
- [fapi.uk payment page](https://fapi.uk/pay)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration guidance]

**Output Format:** [Natural-language summaries, Markdown setup guidance, shell commands, REST API requests, and optional raw JSON when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a fapi.uk API key and Twitter/X credentials; many write actions may require auth_token and ct0 values and consume fapi.uk credits.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
