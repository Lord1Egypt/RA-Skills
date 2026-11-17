## Description:

Provides a YesApi low-code platform wrapper for managing form schemas and performing CRUD and batch operations on form data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phalapi](https://clawhub.ai/user/phalapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect to YesApi, inspect or create form models, add fields, and query, insert, update, or delete records. It is suited to database-management workflows where the operator can provide scoped YesApi credentials and review data-changing actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, update, batch-update, delete, or batch-delete live YesApi records and models.

Mitigation: Use least-privilege credentials, prefer a test account first, and require operator review before destructive or batch operations.

Risk: Credentials may be sent to the configured YESAPI_DOMAIN.

Mitigation: Keep YESAPI_DOMAIN pinned to the legitimate HTTPS YesApi endpoint unless the alternate target is fully trusted.

Risk: The included comprehensive test script performs live create, update, and delete operations.

Mitigation: Do not run test_yesapi.py against production data or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phalapi/skills/crawhub-skill-yesapi)
- [ClawHub publisher profile](https://clawhub.ai/user/phalapi)
- [YesApi API endpoint](https://api.yesapi.net/)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, API calls]

**Output Format:** [Markdown or text responses with JSON-like API result data, Python snippets, and shell commands when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires YESAPI_APP_KEY, YESAPI_DOMAIN, and YESAPI_SIGN environment configuration before live API use.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
