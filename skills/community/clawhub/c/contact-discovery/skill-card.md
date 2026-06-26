## Description: <br>
Find public contact details for a person or company using Prismfy-powered web search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jernejcicorbin-hub](https://clawhub.ai/user/jernejcicorbin-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, recruiting, partnership, and support teams use this skill to find public contact emails, official contact pages, press or support paths, and company email-format clues before outreach. It is intended for public-evidence contact discovery, not private-data inference or guessed personal emails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms may include person names, company names, and other outreach targets that are sent to Prismfy. <br>
Mitigation: Use the skill only when third-party processing by Prismfy is acceptable, and avoid confidential target lists or sensitive outreach research. <br>
Risk: The skill requires a Prismfy API key. <br>
Mitigation: Store PRISMFY_API_KEY in the agent environment, avoid pasting it into prompts or reports, and rotate it if exposure is suspected. <br>
Risk: Email-format clues can be mistaken for confirmed personal contact details. <br>
Mitigation: Treat pattern clues as weak evidence, require explicit public evidence before reporting an email as found, and keep human review before high-value outreach. <br>


## Reference(s): <br>
- [Lead Contact Finder on ClawHub](https://clawhub.ai/jernejcicorbin-hub/contact-discovery) <br>
- [Prismfy](https://prismfy.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Concise chat summary with a contact verdict, source-backed public evidence, optional shell command examples, and optional JSON report output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PRISMFY_API_KEY plus curl and jq; optional JSON reports include timestamp, skill version, entity status, contact verdict, public emails, contact paths, email-pattern clues, source URLs, and run failure code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
