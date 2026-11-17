## Description:

Collect Amazon seller profile and seller information from a known seller URL. Do not use for product details, listings, or reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to submit known Amazon seller URLs to Dataify Builder, monitor the asynchronous task, and return collected seller profile and seller information as JSON. It is scoped to seller information collection and should not be used for product details, listings, or reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send user-supplied URLs and account credentials to Dataify.

Mitigation: Use only intended Amazon seller URLs, confirm the target before submission when there is ambiguity, and keep DATAIFY_API_TOKEN in an environment variable or approved secret store rather than chat.

Risk: Final-result retrieval depends on external sibling code that is not included in the reviewed artifact.

Mitigation: Review and pin the required task-runtime dependency before installing or executing the skill in a managed environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-amazon-seller)
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and JSON results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a task_id and resume command when final-result monitoring times out or no-wait behavior is requested.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
