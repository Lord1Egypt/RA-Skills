## Description:

Use this skill when the user or another skill/prompt needs the latest AgentLens blogs that have not been seen before; it discovers newly published blogs from the AgentLens public API, fetches each new blog's body, and tracks processed blogs in a local memory file so every blog surfaces exactly once.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and automation prompts use this skill to fetch new AgentLens blog posts once, pass the raw blog body and source link to downstream workflows, and commit processed IDs only after successful consumption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts the public AgentLens API and depends on that endpoint being available and returning complete blog bodies.

Mitigation: On API or body-fetch failures, report the failure or skip only the affected blog without marking it processed so a later run can retry.

Risk: The local deduplication file records processed blog IDs and can affect whether posts resurface in later runs.

Mitigation: Choose the memory-file location deliberately and commit IDs only after the caller confirms the blog was successfully consumed.

## Reference(s):

- [AgentLens public API](https://agentlens-core.archlab.workers.dev)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured blog records with Markdown body content and source links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns only unprocessed blog posts and uses a local memory file to avoid repeats after the caller confirms consumption.]

## Skill Version(s):

0.8.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
