## Description:

Filters public financial-procurement notices by user keywords into bank tender, purchase, award, supplier-solicitation, prequalification, and amendment alerts, then returns a formatted daily digest and open-project list with near-deadline items highlighted.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and sales, procurement, or bid teams use this skill to monitor banking-sector procurement opportunities matching their keywords and receive readable daily reports or active-project lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords, license tokens, and stable local device or account identifiers are sent to a vendor service.

Mitigation: Install only after accepting that data sharing, avoid placing the license directly in cron entries, and treat repeated use from the same machine as linkable by the vendor.

Risk: The payment or installation flow asks the user to run external SkillPay installer commands.

Mitigation: Verify the SkillPay installer source and complete wallet or payment confirmation personally rather than delegating confirmation to an agent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/bankbid-daily-free)
- [BankBid daily service endpoint](https://www.tokendidi.cn/api/bankbid/api/v1/bankbid-daily)
- [Subscription account status page](https://www.tokendidi.cn/bankbid/account)

## Skill Output:

**Output Type(s):** [text, markdown, json, guidance]

**Output Format:** [Terminal Markdown by default; optional JSON containing matched counts, closing-soon items, report URL, and item records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls an external vendor service; results depend on subscription/license status, daily service data, and the user's keywords.]

## Skill Version(s):

1.0.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
