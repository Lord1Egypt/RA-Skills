## Description: <br>
Generate AI-powered lead magnets such as checklists, swipe files, and frameworks that convert visitors into subscribers, with PDF generation and optional AI illustrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nttylock](https://clawhub.ai/user/nttylock) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, founders, and growth teams use this skill to create PDF lead magnets and optionally publish public lead-capture pages through Citedy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish public email-capture pages and may use auto_publish without a separate review step. <br>
Mitigation: Require explicit user approval before publishing or enabling auto_publish, and review generated text and images before sharing public URLs. <br>
Risk: The skill requires a Citedy API key and may access Citedy account, product, referral, and lead-magnet data. <br>
Mitigation: Use a dedicated, revocable API key with the minimum account access needed, avoid storing referral links unless intended, and treat account and product lookups as business data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nttylock/citedy-lead-magnets) <br>
- [Citedy agent registration API](https://www.citedy.com/api/agent/register) <br>
- [Citedy lead magnets API](https://www.citedy.com/api/agent/lead-magnets) <br>
- [Citedy](https://www.citedy.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with HTTP examples, JSON request and response bodies, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Citedy lead magnet IDs, status updates, PDF and preview URLs, public lead-capture URLs, and optional embed code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
