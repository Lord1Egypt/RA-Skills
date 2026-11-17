## Description:

Collects Amazon product reviews from known product URLs through Dataify Builder and returns the final collection results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to submit Dataify jobs that collect Amazon product review data by product URL and retrieve the resulting JSON.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Dataify API token for external jobs.

Mitigation: Install and run it only when the Dataify publisher and service are trusted, keep DATAIFY_API_TOKEN in the environment, and never expose the token in chat or logs.

Risk: The skill depends on a sibling dataify-task-operations runtime for final-result retrieval.

Mitigation: Review and trust that runtime before use, and preserve the returned task_id so work can resume without resubmitting a paid job.

Risk: The promised Amazon-only URL scope is not fully enforced by the artifact.

Mitigation: Require known Amazon product URLs and confirm the target URL before submission until URL validation is tightened.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-amazon-comment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON task or result output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task_id for resume or no-wait behavior; by default it waits for and returns the final collected JSON result.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
