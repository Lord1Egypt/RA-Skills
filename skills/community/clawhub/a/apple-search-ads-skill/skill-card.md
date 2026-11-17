## Description:

Manage Apple Search Ads campaigns, ad groups, keywords, and reports via the asa-cli tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trebuhs](https://clawhub.ai/user/trebuhs)

### License/Terms of Use:


## Use Case:

External marketers, app growth teams, and agents working for them use this skill to manage Apple Search Ads campaign structure, keyword bids, account configuration, and performance reporting through asa-cli.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward live Apple Search Ads changes, including create, budget, status, and delete operations.

Mitigation: Require explicit user confirmation with the exact organization ID and resource IDs before executing any create, budget, status, or delete command.

Risk: Apple Search Ads credentials, private key paths, and token cache files may be exposed through prompts, logs, or command output.

Mitigation: Protect ASA credentials and token files, avoid pasting secrets into prompts, and avoid verbose logging unless the output is reviewed and redacted.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-output recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may reference Apple Search Ads organization IDs, campaign IDs, ad group IDs, keyword IDs, date ranges, filters, pagination, output flags, and asa-cli credential configuration values.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
