## Description:

Searches Douyin for influencers matching follower and engagement criteria, reviews their profiles and recent content, sends personalized direct messages, and tracks contacted accounts to avoid duplicates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangtao19911111](https://clawhub.ai/user/wangtao19911111)

### License/Terms of Use:

MIT-0

## Use Case:

External growth and marketing operators use this skill to find small Douyin creators, evaluate recent content and engagement, draft personalized outreach, send DMs from a logged-in account, and keep a contact log.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real outbound Douyin direct messages from a logged-in account.

Mitigation: Require manual review and approval of each recipient and message before sending, and set strict per-run and daily send limits.

Risk: Contact records may contain profile details, message text, and outreach status with weak safeguards.

Mitigation: Store the CSV in a protected location, limit access, and define retention and deletion rules before use.

Risk: Scraped profile text or generated message content may be used in shell commands or scripts.

Mitigation: Avoid passing scraped text into shell commands or generated scripts; when recording data, quote and escape fields carefully.

Risk: Automated outreach can create privacy, platform-policy, or marketing-compliance risk.

Mitigation: Use the skill only within Douyin rules and applicable local privacy and marketing requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangtao19911111/skills/douyin-influencer-outreach)
- [Usage examples](artifact/examples.md)
- [Douyin search URL pattern](https://www.douyin.com/jingxuan/search/{keyword}?type=general)
- [Douyin profile URL pattern](https://www.douyin.com/user/{sec_uid})

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser actions, shell commands, JavaScript snippets, message templates, and CSV contact records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before outreach and produces personalized DM text plus contact-tracking records.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
