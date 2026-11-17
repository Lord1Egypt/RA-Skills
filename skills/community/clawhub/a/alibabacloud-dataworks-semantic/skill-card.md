## Description:

Guides agents through Alibaba Cloud DataWorks semantic analysis job workflows, including readiness checks, create/run/stop operations, monitoring, diagnostics, and controlled result downloads through the public DataWorks OpenAPI CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and cloud operators use this skill to safely operate Alibaba Cloud DataWorks semantic analysis jobs backed by MaxCompute, Hologres, StarRocks, or existing CSV/XLSX references. It supports exact job resolution, controlled state-changing operations, bounded monitoring, sanitized diagnostics, and result retrieval without exposing presigned artifact URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use an active Aliyun CLI profile to create or run jobs that consume compute, stop a specific run, and download result artifacts that may contain sensitive data.

Mitigation: Review cloud permissions before use, grant only the workflow-specific DataWorks actions, require exact operation identifiers for state-changing calls, and avoid wildcard data-plane permissions where narrower authorization is available.

Risk: Downloaded result responses can contain presigned artifact URLs that function as temporary credentials.

Mitigation: Capture the download response once into an owner-only temporary file, use the bundled downloader to validate HTTPS Alibaba Cloud URLs and safe local paths, and never print URL query strings or attach Aliyun credentials to artifact downloads.

Risk: Ambiguous retries after timeouts could duplicate jobs, submit extra runs, or repeat stop requests.

Mitigation: Query current job or executor state before retrying, preserve JobRunId and ExecutorJobId separately, and report unconfirmed bounded-wait outcomes instead of blindly repeating state-changing operations.

## Reference(s):

- [Command Reference](artifact/references/command-reference.md)
- [RAM Policies](artifact/references/ram-policies.md)
- [Verification Method](artifact/references/verification-method.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands, JSON snippets, identifiers, status outcomes, and file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports sanitized run context, terminal or bounded-wait outcomes, downloaded artifact names, and local destination paths; presigned URLs and credential material are excluded.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
