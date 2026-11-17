## Description:

Collect Walmart product records by URL, category URL, SKU, or keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify Builder jobs for Walmart product data collection and to monitor the task until final JSON results are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe credential handling can expose the Dataify API token.

Mitigation: Do not paste API tokens into chat, use the skill only in a contained environment, and rotate the token if it may have been exposed.

Risk: Task status and download authentication place the token in URLs.

Mitigation: Avoid running the bundled scripts until task-status and download authentication no longer put the token in URLs.

Risk: A script import path can run unreviewed local code.

Mitigation: Avoid running the bundled scripts until the external sys.path import is removed or the imported code path is reviewed.

## Reference(s):

- [Modes and Parameters](references/modes-and-parameters.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-walmart-products)
- [Publisher Profile](https://clawhub.ai/user/dataify-server)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task/result payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DATAIFY_API_TOKEN; default behavior waits for final Dataify task results unless no-wait behavior is requested.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
