## Description:

Aliyun OSS (Object Storage Service) file management toolkit for Python that helps agents produce Python guidance for uploading, downloading, listing, reading, deleting, copying, and moving objects with authenticated or anonymous access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill when they need an agent to provide Python examples and operational guidance for managing Aliyun OSS buckets, including object upload, download, listing, metadata lookup, deletion, copy, and move workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-capable examples can upload, delete, copy, or move objects in Aliyun OSS when credentials allow those operations.

Mitigation: Use least-privilege credentials, prefer read-only access when possible, and confirm the intended bucket, endpoint, key, and prefix before running generated code.

Risk: Prefix-based directory operations can affect more objects than intended, especially for delete or move workflows.

Mitigation: List matching objects before delete or move operations and narrow prefixes to the smallest practical scope.

Risk: Upload examples can expose secrets or unintended local files if broad folders or sensitive paths are selected.

Mitigation: Review local paths before upload and exclude credentials, private configuration, and other sensitive files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangyendt/skills/aliyun-oss-2)
- [Publisher profile](https://clawhub.ai/user/wangyendt)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown with Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include bucket endpoint, object key, prefix, credential, verbosity, and local path parameters in generated examples.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
