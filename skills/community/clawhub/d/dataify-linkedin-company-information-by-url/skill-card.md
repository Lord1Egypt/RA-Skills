## Description:

Collects structured LinkedIn company information from one or more known company URLs, excluding personal profiles, jobs, and Crunchbase URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to prepare and execute Dataify Builder requests for collecting company-level LinkedIn data from known company URLs, then wait for and return the final JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is presented as a LinkedIn company URL lookup tool, but its instructions and catalog allow broader Dataify scraping requests with weak validation.

Mitigation: Run it only when scoped to the linkedin_company_information_by-url tool with a real LinkedIn company URL and parameter validation.

Risk: Persistent token setup guidance may expose a Dataify token to this workflow.

Mitigation: Use session-scoped DATAIFY_API_TOKEN setup where possible, never paste tokens into chat, and rotate any token that may have been exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-linkedin-company-information-by-url)
- [Tool parameter catalog](artifact/references/tool-params.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, JSON]

**Output Format:** [Markdown with shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can preview a normalized curl request, submit a Dataify task, return a task ID for no-wait flows, or wait for and return the final collected JSON result.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
