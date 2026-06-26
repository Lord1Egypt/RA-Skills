## Description: <br>
Research a company or person and get actionable sales intel using web search, with optional enrichment and CRM context when connected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rolandpg](https://clawhub.ai/user/rolandpg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and customer-facing teams use this skill to research companies, prospects, and meeting attendees before outreach. It summarizes business profile, recent news, hiring signals, key people, optional enrichment data, CRM history, qualification signals, and recommended outreach angles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may query connected enrichment or CRM systems and surface sensitive contact details, prior relationship history, or internal notes. <br>
Mitigation: Configure least-privilege connectors, require explicit confirmation before CRM or enrichment lookups, and limit display of personal contact details and internal notes by default. <br>
Risk: Natural-language research prompts may produce broad account lookups that include personal data not needed for the immediate outreach task. <br>
Mitigation: Ask users to specify the target company, person, and goal, and keep the final brief focused on business-relevant facts and cited sources. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rolandpg/account-research) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/rolandpg) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown research brief with tables, bullets, source links, and recommended outreach guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include web-search findings, optional enrichment contact details, optional CRM relationship history, qualification signals, and cited sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
