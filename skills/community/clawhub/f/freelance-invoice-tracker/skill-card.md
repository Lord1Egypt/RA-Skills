## Description: <br>
Automated invoice tracking and payment follow-up for Indian freelancers using Google Sheets, email or WhatsApp reminders, GST tracking, and monthly income reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[utsavs](https://clawhub.ai/user/utsavs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External freelancers in India use this skill to track invoices, calculate GST summaries, send payment follow-up reminders, and monitor receivables from a Google Sheet. <br>

### Deployment Geography for Use: <br>
India <br>

## Known Risks and Mitigations: <br>
Risk: Google service account credentials and invoice sheet access can expose client, invoice, and payment data if over-scoped or shared carelessly. <br>
Mitigation: Limit the service account to the intended invoice sheet and keep credentials out of files, chats, and generated content. <br>
Risk: Automated reminders can contact the wrong recipient or send a message that is too early, too firm, or routed through the wrong channel. <br>
Mitigation: Review reminder templates, recipients, overdue tiers, and email or WhatsApp channels before enabling automated sends. <br>
Risk: GST summaries may be mistaken for tax filing or professional tax advice. <br>
Mitigation: Use the summaries as tracking aids only and consult a qualified tax professional for GST filing decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/utsavs/freelance-invoice-tracker) <br>
- [Google Sheets API v4 endpoint](https://sheets.googleapis.com/v4/spreadsheets/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown text with invoice summaries, reminder message templates, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GOOGLE_SHEETS_CREDENTIALS and INVOICE_SHEET_ID; email, WhatsApp, and reminder behavior should be reviewed before automation.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
