## Description: <br>
Agency Workflow Starter helps agents guide users through importing and configuring a pre-built n8n inbound lead routing workflow for agency lead handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[celestchief](https://clawhub.ai/user/celestchief) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI automation agencies, freelancers, and developers use this skill to deploy a client-ready inbound lead router that scores, deduplicates, logs, and routes form submissions through n8n. It is intended for users who will manually import the workflow and connect their own CRM, Sheets, Airtable, and optional Slack credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow accepts inbound lead data through a webhook and may be exposed to spam, abuse, or malformed submissions. <br>
Mitigation: Add webhook abuse controls and validate or sanitize submitted fields before using the workflow with live or client leads. <br>
Risk: Lead records can contain personal or client data and may be forwarded to Sheets, Airtable, HubSpot, or Slack. <br>
Mitigation: Use least-privilege credentials, restrict access to downstream destinations, and confirm consent, retention, and privacy obligations before production use. <br>
Risk: Routing and scoring rules are template defaults that may not match a client's qualification model. <br>
Mitigation: Review and test threshold logic, duplicate checks, CRM lookup behavior, and notification destinations before activating the workflow. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/celestchief/agency-workflow-starter) <br>
- [Publisher profile](https://clawhub.ai/user/celestchief) <br>
- [Agency Growth Pack upgrade](https://qssys.gumroad.com/l/AgencyGrowthAutomationPack) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with references to an importable n8n workflow JSON file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Directs users to import lead-router.json and configure n8n webhook, CRM or Sheets, and optional Slack destinations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
