## Description:

Collect eBay product records by product URL, category URL, keyword, or store URL. Do not use for Amazon, Walmart, or general shopping-search results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs for eBay product collection by product URL, category URL, keyword, or store URL, then wait for the final collected JSON result.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper script imports code from a nearby dataify-task-operations runtime that is outside this skill artifact and can pass that code the user's Dataify API TOKEN.

Mitigation: Review the sibling runtime before installation or execution, use a session-scoped DATAIFY_API_TOKEN, and do not paste tokens into chat.

Risk: Running the skill submits requests to Dataify Builder and may consume account credits for eBay product collection.

Mitigation: Confirm the selected collection mode, target URLs or keywords, and expected scope before running high-volume or multi-input jobs.

## Reference(s):

- [Modes and parameters](references/modes-and-parameters.md)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-ebay-products)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task or result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task identifier and status during submission, or the final collected JSON result after asynchronous monitoring completes.]

## Skill Version(s):

1.3.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
