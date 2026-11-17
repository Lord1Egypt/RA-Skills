## Description:

Run a complete cold email outreach campaign from sourcing leads to handling replies, including ICP definition, lead sourcing, email sequence construction, personalization, reply handling, and suppression management without paid tools or SaaS subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[celestchief](https://clawhub.ai/user/celestchief)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, growth, and operations teams use this skill to plan and run cold email outreach using free-tier tools. It guides an agent through defining an ICP, sourcing and cleaning leads, drafting a multi-touch sequence, sending or automating follow-ups, handling replies, and maintaining suppression lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables broad automated outreach and contact data processing without enough built-in compliance and consent safeguards.

Mitigation: Use it only with contacts you are allowed to process and email, require human approval before importing lead lists or sending outbound sequences, and honor opt-outs immediately.

Risk: Contact records, suppression lists, and campaign status may be stored in shared spreadsheets.

Mitigation: Restrict Google Sheet sharing, keep suppression lists current, and review access before adding or exporting lead data.

Risk: Gmail, SMTP, Google Sheets, or n8n credentials may be needed for execution.

Mitigation: Store credentials only in secure credential stores and review the skill before allowing an agent to execute workflows.

## Reference(s):

- [Lead Sourcing Reference](references/lead-sourcing.md)
- [Email Sequences Reference](references/email-sequences.md)
- [Reply Handling Reference](references/reply-handling.md)
- [Tools — Free Tier Setup Guide](references/tools-free-tier.md)
- [Cold Outreach System](https://qssys.gumroad.com/l/cold-outreach-system)
- [ClawHub skill page](https://clawhub.ai/celestchief/skills/cold-outreach-free)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with templates, tables, checklists, and inline setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include outreach copy, lead sourcing criteria, spreadsheet structure, reply playbooks, and optional n8n setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md metadata, _meta.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
