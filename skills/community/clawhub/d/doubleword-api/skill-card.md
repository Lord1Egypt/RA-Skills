## Description:

Create, submit, monitor, and retrieve asynchronous batch AI inference jobs via the Doubleword API using JSONL files for large or cost-sensitive workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjb157](https://clawhub.ai/user/pjb157)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to prepare JSONL batch request files, submit them to Doubleword's external API, monitor asynchronous batch jobs, and download result or error files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Batch JSONL files may contain sensitive prompts or other data uploaded to Doubleword's external API.

Mitigation: Review files before upload and avoid secrets, regulated data, or confidential data unless Doubleword processing is approved.

Risk: The DOUBLEWORD_API_KEY credential could be exposed through shell history, logs, or shared configuration.

Mitigation: Manage DOUBLEWORD_API_KEY as a sensitive API credential and avoid embedding it directly in files or shared command transcripts.

Risk: Downloaded result and error JSONL files may contain sensitive model outputs or request context.

Mitigation: Store and share downloaded output and error files according to the data sensitivity of the submitted batch.

## Reference(s):

- [Doubleword Batch API Reference](references/api_reference.md)
- [Doubleword API base URL](https://api.doubleword.ai/v1)
- [ClawHub skill page](https://clawhub.ai/pjb157/skills/doubleword-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON, JSONL, Python, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing instructions for external API use; it does not execute API calls by itself.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
