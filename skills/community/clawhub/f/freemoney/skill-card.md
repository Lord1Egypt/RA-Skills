## Description:

Freemoney helps Chinese-speaking users query open class-action settlement claims in the United States, Canada, the United Kingdom, and Australia, including no-proof claim opportunities and application guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adsorgcn](https://clawhub.ai/user/adsorgcn)

### License/Terms of Use:

MIT-0

## Use Case:

External Chinese-speaking users use this skill to find potentially relevant class-action settlement claims, filter no-proof claims, and receive Chinese guidance for where to apply. The skill is positioned as a passive lookup tool that retrieves settlement data only when the user asks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill points users to class-action claim opportunities where eligibility errors or false submissions can create legal or financial risk.

Mitigation: Verify eligibility and claim details on the official claim site before submitting, and apply only for claims where the user genuinely meets the stated criteria.

Risk: The reviewed skill mentions external setup paths, a separate freemoney-plugin, Tencent Cloud, DeepSeek, and a QQ support group that were not reviewed as part of this release evidence.

Mitigation: Treat those external resources as unaudited, avoid sharing API keys or credentials in chat or support groups, and review them separately before use.

Risk: The skill depends on an external read-only API for settlement data, so results can be unavailable, stale, incomplete, or superseded by official claim administrators.

Mitigation: Use API results as a starting point and confirm deadlines, eligibility, amounts, and submission instructions against official claim pages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adsorgcn/skills/freemoney)
- [Publisher profile](https://clawhub.ai/user/adsorgcn)
- [I-Lang homepage](https://ilang.ai)
- [Claims API stats endpoint](https://api.ilang.ai/claims/api/stats)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Chinese Markdown responses with tables, settlement details, claim links, and short safety reminders]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses read-only GET requests to api.ilang.ai after user confirmation; the reviewed skill does not provide proactive push behavior.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
