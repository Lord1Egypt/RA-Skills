## Description:

Helps agents access Cognito Forms through a connected Maton account to list forms, manage entries, and retrieve submissions and documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

People and teams use this skill to review Cognito Forms submissions, manage form entries, and retrieve associated documents with their authorized account. Approved automations can also run those actions on a schedule or in response to events from other connected apps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to the wrong account or more form data than the task needs.

Mitigation: Confirm the account and connection, choose read-only scopes where possible, and retrieve only the necessary fields.

Risk: Entry changes or deletions can alter or remove submitted data.

Mitigation: Start with read-only operations and confirm the exact target and intended effect before every write or deletion.

Risk: Persistent automations or third-party destinations may forward event data over time.

Mitigation: Approve each automation separately and use third-party destinations only after confirming the data shared and how long forwarding continues.

## Reference(s):

- [Cognito Forms API Overview](https://www.cognitoforms.com/support/475/data-integration/cognito-forms-api)
- [Maton homepage](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [Maton CLI manual](https://cli.maton.ai/manual)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown with command examples and structured API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected account, connection permissions, and Cognito Forms API responses.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
