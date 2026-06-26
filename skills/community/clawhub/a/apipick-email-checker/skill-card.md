## Description: <br>
Validate email addresses using the apipick Email Validator API, including syntax checks, MX record verification, and disposable email detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to check whether an email address has valid syntax, whether its domain can receive mail, and whether it appears to be disposable before using it in workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email addresses checked with this skill are sent to the apipick API. <br>
Mitigation: Use the skill only for email addresses you are authorized to validate and review apipick's privacy and retention terms before checking sensitive or bulk personal email lists. <br>
Risk: The skill requires an apipick API key. <br>
Mitigation: Provide the key through the APIPICK_API_KEY environment variable and avoid pasting long-lived credentials into chat. <br>


## Reference(s): <br>
- [apipick Email Validator API Reference](references/api_reference.md) <br>
- [apipick API Platform](https://www.apipick.com) <br>
- [Email Validator Product Page](https://www.apipick.com/check-email) <br>
- [apipick API Keys](https://www.apipick.com/dashboard/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with optional shell command examples and structured API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIPICK_API_KEY and sends submitted email addresses to the apipick API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
