## Description: <br>
Run a complete cold email outreach campaign from lead sourcing through reply handling, including ICP definition, lead sourcing strategy, email sequence construction, personalization, suppression management, and optional n8n automation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CelestChief](https://clawhub.ai/user/CelestChief) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, sales operators, founders, and agents use this skill to plan and execute a low-cost cold email outreach workflow. It produces structured guidance for sourcing leads, writing and sending a three-touch sequence, tracking status in spreadsheets, handling replies, and maintaining suppression lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support unsolicited outreach and contact-data handling without strong safeguards. <br>
Mitigation: Use it only for lawful outreach where data-source permissions, anti-spam requirements, opt-out language, suppression handling, and retention limits have been reviewed. <br>
Risk: An agent or workflow could send live emails before the campaign is approved. <br>
Mitigation: Require human approval of the lead list, message copy, sending schedule, and volume before any email is sent. <br>
Risk: Imported n8n workflows or sending credentials could expand operational risk. <br>
Mitigation: Use a dedicated sending account with revocable credentials and inspect any external n8n workflow JSON before importing it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CelestChief/cold-outreach-free) <br>
- [Lead Sourcing Reference](references/lead-sourcing.md) <br>
- [Email Sequences Reference](references/email-sequences.md) <br>
- [Reply Handling Reference](references/reply-handling.md) <br>
- [Tools Free Tier Setup Guide](references/tools-free-tier.md) <br>
- [Cold Outreach System product page](https://qssys.gumroad.com/l/cold-outreach-system) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with checklists, tables, templates, and inline shell commands where n8n setup is discussed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces campaign plans, email copy, lead-list fields, tracking-sheet status guidance, reply playbooks, suppression handling steps, and optional n8n setup instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence, SKILL.md frontmatter, _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
