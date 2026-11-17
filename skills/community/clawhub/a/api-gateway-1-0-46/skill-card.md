## Description:

Connects agents to 100+ third-party APIs through Maton's managed OAuth gateway, enabling native API calls for services such as Google Workspace, Microsoft 365, Notion, Slack, Airtable, and HubSpot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mbright4497](https://clawhub.ai/user/mbright4497)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to let agents call authorized third-party SaaS APIs and manage Maton OAuth connections with documented API patterns and code examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can act broadly across authorized Maton-managed third-party service connections.

Mitigation: Authorize only the services and OAuth scopes needed for the intended task, and review connected-account access before deployment.

Risk: Documented API examples include deletes, live sends, admin changes, billing actions, and public posts that can have external effects.

Mitigation: Require explicit user confirmation before destructive, financial, administrative, or public-facing API calls.

Risk: MATON_API_KEY values and connection URLs can expose access to the gateway or connection setup flows.

Mitigation: Treat MATON_API_KEY and connection URLs as secrets and avoid printing, logging, sharing, or pasting them into transcripts.

## Reference(s):

- [Maton Homepage](https://maton.ai)
- [Maton API Reference](https://www.maton.ai/docs/api-reference)
- [Slack Routing Reference](references/slack.md)
- [Gmail Routing Reference](references/google-mail.md)
- [Google Sheets Routing Reference](references/google-sheets.md)
- [Notion Routing Reference](references/notion.md)
- [Airtable Routing Reference](references/airtable.md)
- [HubSpot Routing Reference](references/hubspot.md)
- [Microsoft Teams Routing Reference](references/microsoft-teams.md)
- [Salesforce Routing Reference](references/salesforce.md)
- [Stripe Routing Reference](references/stripe.md)
- [QuickBooks Routing Reference](references/quickbooks.md)
- [GitHub Routing Reference](references/github.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with endpoint patterns and Python, JavaScript, and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and user-authorized OAuth connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
