## Description:

Helps agents use the Eudic OpenAPI to query, add, update, and delete vocabulary lists, words, corpus entries, and notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lulu-trans](https://clawhub.ai/user/lulu-trans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to manage Eudic, French Assistant, German Assistant, and Spanish Assistant vocabulary data through authenticated OpenAPI calls. It supports account-level read and write workflows for study lists, words, user corpus entries, and notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can propose API calls that read or change vocabulary lists, words, user corpus entries, and notes using the user's Eudic OpenAPI token.

Mitigation: Have the agent show the exact target and operation before write or delete requests, and require explicit confirmation for destructive actions.

Risk: An exposed API token may allow account-level access to Eudic data.

Mitigation: Keep the token out of shared logs and prompts where possible, and revoke or rotate it if exposure is suspected.

Risk: Repeated API calls may trigger documented Eudic rate limits and temporary blocking.

Mitigation: Batch requests where supported, avoid retry loops, and slow down calls when rate-limit responses occur.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/lulu-trans/skills/eudic-openapi-skills)
- [Eudic OpenAPI authorization](https://my.eudic.net/OpenAPI/Authorization)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [Markdown guidance with curl command examples and JSON request shapes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Eudic OpenAPI token; proposed calls may read or modify account data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
