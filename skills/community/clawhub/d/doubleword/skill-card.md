## Description:

Submit and manage asynchronous batch AI inference jobs with the Doubleword API, including OpenAI-compatible endpoints, tool calling, structured outputs, and JSONL batch workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pjb157](https://clawhub.ai/user/pjb157)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to create JSONL batch request files, submit asynchronous Doubleword inference jobs, monitor status, download results, and handle errors for large-scale workloads that do not require immediate responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded prompts and downloaded results may contain sensitive data processed by a third-party service.

Mitigation: Do not include secrets, credentials, regulated data, or sensitive personal data unless approved by the user's organization, and protect downloaded results and error files.

Risk: Doubleword API keys can expose account access if committed, logged, or shared.

Mitigation: Store API keys in environment variables or a secrets manager, rotate keys periodically, and avoid committing keys to version control.

Risk: Malformed JSONL, duplicate custom IDs, oversized files, or incomplete batch downloads can lead to failed or partial results.

Mitigation: Validate JSONL locally, keep files under documented limits, use unique custom IDs, monitor batch status, and check error files and incomplete-result headers before relying on outputs.

Risk: Installing the optional autobatcher package introduces a third-party Python dependency.

Mitigation: Review and manage the dependency according to the organization's normal third-party package approval process.

## Reference(s):

- [Doubleword Batch API Reference](references/api_reference.md)
- [Getting Started with Doubleword Batch API](references/getting_started.md)
- [Doubleword Batch API Pricing](references/pricing.md)
- [Doubleword Batch Documentation](https://docs.doubleword.ai/batches)
- [autobatcher Python Client](https://github.com/doublewordai/autobatcher)
- [Doubleword Console](https://app.doubleword.ai/)
- [ClawHub Skill Page](https://clawhub.ai/pjb157/skills/doubleword)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions, Files]

**Output Format:** [Markdown with bash, JSON, JSONL, and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of local JSONL batch request files and retrieval of results.jsonl or errors.jsonl files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
