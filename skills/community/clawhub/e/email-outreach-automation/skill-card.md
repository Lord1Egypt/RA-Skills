## Description:

Cold email outreach pipeline with multi-step sequences, reply tracking, bounce handling, and campaign analytics. 4 production-ready n8n workflows with Google Sheets CRM and SMTP integration.

This skill is for research and development only.

## Publisher:

[mhmalvi](https://clawhub.ai/user/mhmalvi)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Developers, operators, agencies, founders, recruiters, and sales teams use this skill to import prospects, run sequenced outreach, track replies, and receive campaign analytics in a self-hosted n8n setup backed by Google Sheets and SMTP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public webhooks can modify prospect records or trigger notifications without sufficient safeguards.

Mitigation: Use a strong OUTREACH_SECRET, fail closed when it is missing, add webhook authentication or signature verification, and enforce rate limits and request-size limits.

Risk: Automated outreach can be misused with unlawful or non-consent-aware prospect lists.

Mitigation: Use only lawful, consent-aware prospect lists and maintain suppression and opt-out handling before activating campaigns.

Risk: Google Sheets and SMTP credentials can expose prospect data or sending capability if over-privileged.

Mitigation: Restrict Google Sheets and SMTP credentials to the minimum permissions and accounts needed for the outreach workflows.

Risk: Reply content and report recipients can expose sensitive information if handled unsafely.

Mitigation: Validate admin report recipients and avoid rendering raw reply content as HTML.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mhmalvi/skills/email-outreach-automation)
- [Skill Definition](artifact/SKILL.md)
- [Prospect Import Workflow](artifact/workflows/01-prospect-import.json)
- [Outreach Sequence Workflow](artifact/workflows/02-outreach-sequence.json)
- [Reply Tracker Workflow](artifact/workflows/03-reply-tracker.json)
- [Campaign Report Workflow](artifact/workflows/04-campaign-report.json)

## Skill Output:

**Output Type(s):** [JSON, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown guidance with n8n workflow JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires n8n v2.4+, Google Sheets OAuth2 credentials, SMTP credentials, OUTREACH_SECRET, and OUTREACH_ADMIN_EMAIL.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
