## Description: <br>
Provides GoHighLevel CRM API v2 automation for contacts, conversations, notes, opportunities, calendars, tags, tasks, forms, workflows, payments, and invoices, with rate-limit retries, safety guardrails, and real-time conversation support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brianxmacdonald](https://clawhub.ai/user/brianxmacdonald) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and CRM automation teams use this skill to let an agent read and update GoHighLevel records, manage lead conversations, log notes, move opportunities, inspect calendars, and trigger approved workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send customer messages and change CRM records with broad GoHighLevel token access and no built-in per-action approval. <br>
Mitigation: Use the least-privileged token possible, start in a test location, and require human approval outside the skill for outbound messages and important CRM changes. <br>
Risk: Outbound SMS and workflow automation can create consent, timing, or compliance exposure. <br>
Mitigation: Verify TCPA and consent handling before allowing SMS or workflow automation, and keep bulk messaging behind human approval. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brianxmacdonald/ghl) <br>
- [SetupClaw homepage](https://setupclaw.tech) <br>
- [GoHighLevel API endpoint](https://services.leadconnectorhq.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python CLI commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 plus GHL_API_KEY and GHL_LOCATION_ID environment variables.] <br>

## Skill Version(s): <br>
1.3.0 (source: SKILL.md frontmatter, _meta.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
