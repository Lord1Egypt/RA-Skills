## Description:

Summarizes public Alipay product features, announcements, and city service updates without login, payment, or private account actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to collect concise summaries of public Alipay service pages, announcements, news items, and city service updates. It is limited to public information and excludes account support, logged-in sessions, payment operations, identity verification, and private financial data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill could be misapplied to account support, payments, identity verification, logged-in sessions, or user-specific financial information.

Mitigation: Use it only for public Alipay page summaries and announcement monitoring, and reject tasks involving private accounts, payments, identity checks, or user-specific financial data.

Risk: Dynamic public pages and access-rate limits can lead to incomplete or outdated summaries.

Mitigation: Wait for page loading, include source links and collection time in summaries when available, and respect platform access limits.

## Reference(s):

- [Alipay homepage](https://www.alipay.com/)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/alipay-hot-trend)
- [ClawHub publisher profile](https://clawhub.ai/user/codekungfu)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain-text summaries with extracted links and timestamps when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service names, feature summaries, announcement titles, publication times, impact scope, source links, city names, and collection time.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
