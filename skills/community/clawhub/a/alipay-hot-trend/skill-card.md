## Description: <br>
Summarizes public Alipay product features, announcements, and city service updates without login or payment actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CodeKungfu](https://clawhub.ai/user/CodeKungfu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and analysts use this skill to summarize public Alipay product, announcement, news, and city service pages for monitoring and internal analysis. It should not be used for login, payments, account support, authenticated content, or bypassing platform limits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill on authenticated Alipay pages or payment flows could expose account data or trigger unintended actions. <br>
Mitigation: Use it only for public pages and announcements; do not use it for login, payment, account-specific support, authenticated content, or bypassing platform limits. <br>
Risk: Summaries of dynamic public pages may be incomplete or stale if content has not fully loaded. <br>
Mitigation: Wait for pages to load, include source links and collection time when available, and review summaries before relying on them. <br>
Risk: High-frequency automated access may violate Alipay platform limits. <br>
Mitigation: Rate-limit requests and respect platform access limits. <br>


## Reference(s): <br>
- [Alipay homepage](https://www.alipay.com/) <br>
- [ClawHub skill page](https://clawhub.ai/CodeKungfu/alipay-hot-trend) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown summaries and structured lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are limited to public Alipay pages and announcements; no account, login, or payment actions.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
