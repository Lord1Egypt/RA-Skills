## Description:

Query FreshBooks invoices, clients, estimates, payments, expenses, projects, and time tracking from a shell using curl and a rotating OAuth token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation authors use this skill to retrieve FreshBooks business data from shell scripts. It also provides examples for creating or updating records and emailing clients through FreshBooks API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The request wrapper may send an OAuth access token to a host outside FreshBooks if request destinations or curl options are not constrained.

Mitigation: Restrict requests to the FreshBooks HTTPS API host and allow only reviewed request options; protect token output and credential files.

Risk: API writes and emails can change financial records or contact recipients, and some example write recipes are unverified.

Mitigation: Use only the necessary read scopes where possible. Before a change or email, confirm the account, records, amounts, and recipients; replace example IDs and re-read records to verify changes.

Risk: Refresh tokens rotate and are single-use, so concurrent use of one state file or failure to save a replacement can interrupt account access.

Mitigation: Use a single tool with its own protected state file for each token stream, and persist each rotated token before continuing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chrischall/skills/freshbooks-mcp)
- [FreshBooks API scopes](https://www.freshbooks.com/api/scopes)
- [FreshBooks developer app registration](https://my.freshbooks.com/#/developer)
- [Recipes and API examples](artifact/references/recipes.md)
- [OAuth bootstrap script](artifact/references/fb-bootstrap.mjs)
- [OAuth token helper](artifact/references/fb-token.sh)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Code, Guidance]

**Output Format:** [Markdown with shell commands, JSON request examples, and jq response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [FreshBooks API responses are returned as JSON; available data and actions depend on the connected account and OAuth permissions.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
