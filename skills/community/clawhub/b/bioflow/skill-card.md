## Description:

Quick guide for BioFlow backend API usage and integration, covering signup/login, file upload/download, token balance query, task submission, and result retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashipiling](https://clawhub.ai/user/ashipiling)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to produce a compact BioFlow API quickstart covering account setup, authentication, dataset transfer, token balance checks, PTMPred task submission, polling, and result download.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes examples for login tokens, dataset upload, balance checks, and chargeable task submission.

Mitigation: Review real hosts, credentials, files, and job requests before allowing an agent to execute the API calls.

Risk: API guidance may become stale if BioFlow endpoints or authentication behavior change.

Mitigation: Check the current API host documentation before using generated requests in production workflows.

## Reference(s):

- [BioFlow API Call Flow](references/api-call-flow.md)
- [BioFlow Project Snapshot](references/current-auth-map.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration instructions]

**Output Format:** [Markdown with endpoint summaries and minimal request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Concise responses focused on one demo algorithm path and current Bearer token flow]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
