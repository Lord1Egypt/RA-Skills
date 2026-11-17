## Description:

Collect structured Airbnb listing results from a known Airbnb search-results URL through Dataify.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect structured Airbnb listing results from a provided Airbnb search URL, submit the Dataify Builder task, monitor completion, and return the final collected JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill as suspicious because an Airbnb-specific description is packaged with broader scraping and workflow code.

Mitigation: Review before installation and remove or isolate unrelated business workflow scripts if only Airbnb search-result collection is needed.

Risk: Credential handling can expose or over-retain a Dataify API token if users paste tokens into chat or store broad tokens permanently.

Mitigation: Use a limited Dataify token, never paste it into chat, avoid permanent shell-profile storage when unnecessary, and rotate or review the key if it is rejected.

Risk: Generated curl commands or edited URLs can initiate paid Dataify requests against untrusted or unintended targets.

Mitigation: Review the target URL and generated command before execution, use only trusted complete HTTP(S) Airbnb search URLs, and avoid executing commands for untrusted or edited URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-airbnb-product-by-searchurl)
- [Tool parameter catalog](artifact/references/tool-params.json)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Dataify API token and a valid Airbnb search URL; may return a task ID and resume command if monitoring times out.]

## Skill Version(s):

1.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
