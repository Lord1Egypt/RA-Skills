## Description:

Daily Learning standardizes a recurring agent workflow for studying one topic at a time, writing structured local notes, optionally submitting learning output to a shared wiki, verifying completion, and completing a post-learning review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and agent operators use this skill to set up and run structured daily learning routines, including topic selection, research, note writing, optional wiki ingestion, progress tracking, verification, and review. It is intended for recurring learning workflows rather than one-off Q&A or unstructured information gathering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may persist private workspace context in local learning notes and optional shared wiki submissions.

Mitigation: Limit workspace and conversation access to intentional context, and review or redact notes before wiki ingestion.

Risk: Shared wiki submissions may publish learning output without clear approval boundaries.

Mitigation: Require review before wiki ingestion and keep the optional wiki path scoped to an approved knowledge base.

Risk: External learning requests can change recurring learning priorities.

Mitigation: Restrict who can edit LEARNING-REQUESTS.md and review urgent or interleaved requests before acting on them.

## Reference(s):

- [Learning Template](references/learning-template.md)
- [Post-Learning Template](references/post-learning-template.md)
- [Daily Learning Verification Script](scripts/verify-daily-learning.sh)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local learning notes, progress updates, optional wiki-ingest markdown, verification output, and post-learning review guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
