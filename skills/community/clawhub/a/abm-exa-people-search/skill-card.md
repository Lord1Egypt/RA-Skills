## Description: <br>
Helps users find specific people at companies or discover who holds certain roles using Exa similarity search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mariokarras](https://clawhub.ai/user/mariokarras) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to identify specific individuals by company, role, or profile for outreach, research, hiring, or partnership work. It is intended for finding the right person, not for building broad company prospect lists. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: People-search queries, company names, roles, and profile URLs may be sent to Exa through the referenced CLI. <br>
Mitigation: Use the skill only when that data sharing is acceptable, and avoid submitting sensitive personal or confidential business information. <br>
Risk: The skill depends on a local tools/clis/exa.js CLI whose source is outside the provided artifact. <br>
Mitigation: Confirm the CLI comes from a trusted source before using commands produced by the skill. <br>
Risk: The skill may read local product-marketing context files for task context. <br>
Mitigation: Keep secrets and sensitive internal details out of those context files unless they are approved for this workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mariokarras/abm-exa-people-search) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with tables, person-detail sections, and inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results should include target context, count found, name, title, company, profile URL, key information, background when available, and relevance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
