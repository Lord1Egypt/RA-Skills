## Description:

Validate email addresses using the apipick Email Validator API, including syntax checks, MX record verification, and disposable/throwaway email detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

External users, developers, and operations teams use this skill to ask an agent to validate email addresses, confirm whether domains can receive mail, and flag disposable addresses through the apipick API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email addresses submitted for validation are sent to apipick with the user's API key.

Mitigation: Avoid submitting sensitive or regulated personal email data unless the user is comfortable with apipick processing it.

Risk: Each successful validation request consumes apipick account credits.

Mitigation: Confirm the user intends to spend credits before validating large batches or repeated requests.

Risk: The skill depends on a user-provided API key.

Mitigation: Use the APIPICK_API_KEY environment variable and avoid displaying or storing the key in conversation output.

## Reference(s):

- [apipick Email Validator API Reference](references/api_reference.md)
- [apipick API Platform](https://www.apipick.com)
- [Email Validator Product Page](https://www.apipick.com/check-email)
- [Get apipick API Key](https://www.apipick.com/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, Text]

**Output Format:** [Markdown with inline JSON or bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires APIPICK_API_KEY and consumes one apipick credit per successful validation request.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
