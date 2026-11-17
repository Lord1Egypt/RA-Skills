## Description:

Searches and retrieves US business entity data from official Secretary of State records through the Filed.dev API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mgrantley](https://clawhub.ai/user/mgrantley)

### License/Terms of Use:

MIT-0

## Use Case:

External users, analysts, and agents use this skill to search US business registrations, verify whether an entity exists, review entity status and registered agent details, and retrieve full entity records when a Filed.dev API key is available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that crafted search text can execute local code through the shell search script.

Mitigation: Review or patch the script before broad installation, especially when lookup terms may come from emails, webpages, tickets, or other untrusted sources.

Risk: Passing an API key with --api-key can expose the credential through shell history or process listings.

Mitigation: Prefer FILED_API_KEY in the environment and treat the key as a secret.

Risk: Business names, filing numbers, officer names, and registered agent queries are sent to Filed.dev.

Mitigation: Avoid submitting sensitive lookup terms unless sharing them with Filed.dev is acceptable for the use case.

## Reference(s):

- [Filed API Reference](references/api-docs.md)
- [Filed.dev](https://filed.dev)
- [Filed.dev registration](https://filed.dev/register)
- [Filed.dev pricing](https://filed.dev/pricing)
- [Filed API on RapidAPI](https://rapidapi.com/grantley-holdings-grantley-holdings-default/api/filed2)
- [ClawHub skill page](https://clawhub.ai/mgrantley/skills/filed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FILED_API_KEY or --api-key; formatted output uses jq when available and raw JSON is available with --raw.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
