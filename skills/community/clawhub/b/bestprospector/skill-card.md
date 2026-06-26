## Description: <br>
Prospector searches public web and WHOIS sources for potential customer companies, extracts and validates email contacts, caches results locally, and exports customer lists as JSON or CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xieyz1980](https://clawhub.ai/user/xieyz1980) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and business development users can ask an agent to find prospective companies by keyword and region, review cached leads, and export contact data for compliant follow-up. The skill supports lead discovery and simple lookup, not email sending or full customer relationship management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Collected company and email data can create privacy, compliance, or unwanted-outreach risk if used without review. <br>
Mitigation: Review results before use, protect or purge cached and exported files, and ensure outreach complies with applicable privacy and anti-spam rules. <br>
Risk: Public website and WHOIS scraping can return stale, incomplete, or incorrect contact data. <br>
Mitigation: Validate and manually review important contacts before relying on them for business decisions or outreach. <br>
Risk: Untrusted proxy settings can expose browsing activity or route requests through infrastructure the user does not control. <br>
Mitigation: Use only trusted proxy endpoints and avoid embedding credentials or sensitive data in proxy URLs. <br>


## Reference(s): <br>
- [ClawHub Prospector release](https://clawhub.ai/xieyz1980/bestprospector) <br>
- [Publisher profile](https://clawhub.ai/user/xieyz1980) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files, guidance] <br>
**Output Format:** [Markdown guidance and shell commands, with script outputs in JSON, CSV, or terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated data may be cached locally under cache/ and exported in bulk to user-selected JSON or CSV files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
