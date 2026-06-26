## Description: <br>
Complete cold email outreach system for AI agents. Handles lead generation via Apollo API, email enrichment, Saleshandy sequence creation, prospect import, warmup monitoring, and campaign management. Use when setting up cold outreach, finding decision-maker emails, building email sequences, or managing cold email campaigns. Includes proven email copy templates and deliverability best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[joeytbuilds](https://clawhub.ai/user/joeytbuilds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams, founders, and operators use this skill to have an agent search Apollo, enrich prospect emails, import verified leads into Saleshandy, and monitor warmup before cold outreach campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect prospect emails and add people to outbound campaign systems. <br>
Mitigation: Review lead lists and email copy before import or sending, keep sequences paused by default, and confirm privacy, anti-spam, unsubscribe, suppression-list, and client-confidentiality requirements. <br>
Risk: The skill uses sensitive Apollo and Saleshandy credentials and can spend paid enrichment credits. <br>
Mitigation: Use dedicated limited-scope API keys, avoid command-line secrets, and set strict batch and credit limits before running enrichment or import workflows. <br>
Risk: Activating cold outreach before account readiness can harm deliverability. <br>
Mitigation: Verify SPF, DKIM, and DMARC, require warmup scores of 85 or higher, and start with conservative daily sending limits. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/joeytbuilds/ai-cold-outreach) <br>
- [API Reference](references/api-reference.md) <br>
- [Configuration Template](references/config-template.json) <br>
- [Cold Email Templates](references/email-templates.md) <br>
- [Apollo People Search Endpoint](https://api.apollo.io/api/v1/mixed_people/api_search) <br>
- [Apollo People Match Endpoint](https://api.apollo.io/api/v1/people/match) <br>
- [Saleshandy Open API](https://open-api.saleshandy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and CSV-oriented workflow outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce lead CSV files and trigger third-party outreach imports when credentials are supplied.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
