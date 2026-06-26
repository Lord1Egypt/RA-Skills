## Description: <br>
Search 3.2 billion leaked credentials in the COMB dataset via ProxyNova API (no API key required). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ibnaleem](https://clawhub.ai/user/ibnaleem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Security practitioners and developers use this skill for authorized defensive checks of emails, usernames, or passwords against the COMB leaked-credential dataset through the ProxyNova API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill searches a leaked-credential API and may expose sensitive credential data. <br>
Mitigation: Use only for authorized defensive security work, redact returned credentials, and rotate affected secrets according to organizational policy. <br>
Risk: Submitting live passwords or credentials can disclose sensitive information to an external service. <br>
Mitigation: Do not submit live passwords or credentials that the operator does not own or administer. <br>
Risk: The security summary notes that the skill lacks clear warnings and authorization limits for sensitive queries and results. <br>
Mitigation: Review usage scope before installation and limit access to approved security personnel and approved investigations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ibnaleem/comb) <br>
- [ProxyNova COMB tool](https://www.proxynova.com/tools/comb/) <br>
- [Cybernews COMB coverage](https://cybernews.com/news/largest-compilation-of-emails-and-passwords-leaked-free/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Text] <br>
**Output Format:** [Markdown with inline bash commands and API response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; supports Linux, macOS, and Windows; ProxyNova returns up to 100 results per query and rate limits at about 100 requests per minute.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
