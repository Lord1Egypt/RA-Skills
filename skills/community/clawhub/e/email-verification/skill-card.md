## Description:

Verify email addresses with the BounceBan API, including single and bulk verification for catch-all and SEG-protected emails, quick email or domain checks, credit and rate-limit management, and webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davis-lee](https://clawhub.ai/user/davis-lee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to verify individual email addresses, clean bulk email lists, check address or domain attributes, manage BounceBan credits and rate limits, and process webhook-based verification results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted emails or CSV lists may be shared with BounceBan, including personal or third-party contact data.

Mitigation: Install only when that data sharing is acceptable, get authorization before processing third-party contact lists, and avoid uploading unnecessary CSV columns.

Risk: Bulk exports and webhook callbacks can expose verification results or contact-list data to external locations.

Mitigation: Confirm bulk uploads and exports before running them, treat export URLs as secrets, and use webhooks only with trusted HTTPS endpoints.

Risk: Repeated verification requests or incorrect polling can waste paid credits.

Mitigation: Poll existing verification IDs instead of resubmitting in-flight checks, retry waterfall timeouts according to the skill guidance, and check account credits and rate limits before large jobs.

## Reference(s):

- [BounceBan API Documentation](https://bounceban.com/public/doc/api.html)
- [ClawHub Skill Page](https://clawhub.ai/davis-lee/skills/email-verification)
- [BounceBan API Introduction](references/introduction.md)
- [Single Verification](references/single-verification.md)
- [Bulk Verification](references/bulk-verification.md)
- [Check API](references/check.md)
- [Account API](references/account.md)
- [Webhooks](references/webhooks.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BOUNCEBAN_API_KEY and curl; may call external BounceBan API endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
