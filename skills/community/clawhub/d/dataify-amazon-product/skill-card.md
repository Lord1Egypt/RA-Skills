## Description:

Collect Amazon product details by ASIN or URL, or collect standard product results by keyword, category URL, or Best Sellers URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs for Amazon product detail, keyword result, category listing, and Best Sellers collection, then retrieve the resulting task output when available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Dataify API token and makes external Dataify requests that may consume credits.

Mitigation: Run only after confirming the requested collection scope and use an environment where the token is configured without exposing its value.

Risk: The script imports result-monitoring code from a sibling directory outside the reviewed artifact and passes that code the API token.

Mitigation: Install and run the skill only where the sibling task-runtime dependency is trusted, reviewed, and controlled.

Risk: Localized instructions are inconsistent about whether the skill should stop after task submission or retrieve final results.

Mitigation: Prefer the server-resolved default prompt and English release behavior that wait for asynchronous completion unless the user explicitly requests no-wait behavior.

## Reference(s):

- [Modes and parameters](references/modes-and-parameters.md)
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-amazon-product)
- [Publisher profile](https://clawhub.ai/user/dataify-server)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task or result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses DATAIFY_API_TOKEN and may wait up to 600 seconds by default for final result retrieval.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
