## Description:

Provides an n8n workflow template and setup guidance for capturing, scoring, routing, and logging inbound leads for agency client projects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celestchief](https://clawhub.ai/user/celestchief)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation consultants, and AI agency operators use this skill to import and adapt an n8n inbound lead router for client lead capture workflows. It helps configure webhook intake, lead scoring, CRM or sheet logging, and optional Slack alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow exposes a public webhook that can receive untrusted lead submissions.

Mitigation: Add webhook authentication or upstream protection, validate submitted fields, and length-limit input before routing or storage.

Risk: Personal lead data can be written to Google Sheets and posted to Slack.

Mitigation: Confirm privacy, consent, and retention requirements, use least-privilege credentials, and reduce Slack payloads to the minimum needed.

Risk: Spreadsheet-bound lead fields may contain formulas or other unsafe cell content.

Mitigation: Neutralize spreadsheet formulas and sanitize text before writing lead records to sheets.

Risk: The Dedup Check node is a placeholder and passes all non-empty emails through.

Mitigation: Replace it with a real CRM, Airtable, or sheet lookup or upsert before using the workflow for a client.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/celestchief/skills/agency-workflow-starter)
- [Agency Growth Pack upgrade page](https://qssys.gumroad.com/l/AgencyGrowthAutomationPack)

## Skill Output:

**Output Type(s):** [json, markdown, configuration, guidance]

**Output Format:** [n8n workflow JSON with Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied n8n, CRM or spreadsheet, and optional Slack credentials before activation.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
