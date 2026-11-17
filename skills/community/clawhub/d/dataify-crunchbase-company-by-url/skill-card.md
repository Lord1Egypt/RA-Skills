## Description:

Collect structured Crunchbase company profiles from one or more known company URLs. Do not use for general web research or LinkedIn company URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Crunchbase Builder requests for known Crunchbase company URLs, monitor the asynchronous task, and return the final collected JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Target company URLs, task IDs, and request parameters are sent to Dataify services.

Mitigation: Use only with data that may be shared with Dataify, and review target URLs and parameters before submitting high-volume or sensitive collections.

Risk: The skill depends on DATAIFY_API_TOKEN from the agent environment.

Mitigation: Use a session-scoped token when possible, never paste the token into chat, and rotate it if logs or transcripts may have exposed it.

Risk: The package includes broader business workflow scripts beyond the stated Crunchbase Builder use case.

Mitigation: Deploy the narrow Crunchbase Builder workflow only, or review and remove unrelated broad workflow scripts before installation.

Risk: Waiting on arbitrary task IDs can retrieve or expose results for tasks outside the intended request.

Mitigation: Wait only on task IDs returned from the current submission, and avoid arbitrary task-ID waiting unless access controls and logging are reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-crunchbase-company-by-url)
- [Tool parameters catalog](references/tool-params.json)
- [Dataify Builder endpoint](https://scraperapi.dataify.com/builder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit a Dataify Builder task, wait for completion, and summarize large JSON payloads while preserving raw result access.]

## Skill Version(s):

1.3.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
