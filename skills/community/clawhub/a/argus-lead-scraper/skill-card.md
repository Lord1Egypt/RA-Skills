## Description: <br>
Extracts verified B2B leads (name, email, company, LinkedIn, job title) from target sources and exports them as CRM-ready CSV files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, marketing, and growth teams use this skill to collect, deduplicate, validate, and export targeted B2B lead lists for CRM import. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a live LinkedIn session cookie, which can expose an account if the cookie is logged, shared, or stored insecurely. <br>
Mitigation: Use only a dedicated or low-risk LinkedIn account, treat LI_SESSION/li_at like a password, avoid logging or sharing it, rotate or revoke the session after use, and consider an official API or OAuth-based workflow where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neo1307/argus-lead-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [text, csv, files, guidance] <br>
**Output Format:** [CSV file plus a text summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CSV rows include contact and company fields such as name, job title, company, LinkedIn URL, email, and location.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
